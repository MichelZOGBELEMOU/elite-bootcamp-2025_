"""Network diagnostics derived from configuration."""

from __future__ import annotations

import json
import socket
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import ipaddress

from cli_tool.config import Network


@dataclass
class InterfaceInfo:
    name: str
    addresses: List[str]


def _run_ip_json() -> List[dict]:
    try:
        result = subprocess.run(
            ["ip", "-json", "addr"],
            check=False,
            capture_output=True,
            text=True,
            timeout=3,
        )
        if result.returncode != 0:
            return []
        return json.loads(result.stdout)
    except (FileNotFoundError, subprocess.SubprocessError, json.JSONDecodeError, OSError):
        return []


def _run_ip_route() -> List[str]:
    try:
        result = subprocess.run(
            ["ip", "route", "show"],
            check=False,
            capture_output=True,
            text=True,
            timeout=3,
        )
        if result.returncode != 0:
            return []
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        return []


def collect_interfaces() -> List[InterfaceInfo]:
    interfaces: List[InterfaceInfo] = []
    for iface in _run_ip_json():
        name = iface.get("ifname")
        addresses = []
        for addr in iface.get("addr_info", []):
            local = addr.get("local")
            if local and addr.get("family") in {"inet", "inet6"}:
                addresses.append(local)
        if name:
            interfaces.append(InterfaceInfo(name=name, addresses=addresses))
    return interfaces


def collect_dns_servers(resolv_path: Path = Path("/etc/resolv.conf")) -> List[str]:
    servers: List[str] = []
    try:
        for line in resolv_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("nameserver"):
                parts = line.split()
                if len(parts) >= 2:
                    servers.append(parts[1])
    except (FileNotFoundError, PermissionError, OSError):
        return servers
    return servers


def validate_subnets(interfaces: List[InterfaceInfo], networks: Dict[str, Network]) -> List[str]:
    warnings: List[str] = []
    all_ips = [addr for iface in interfaces for addr in iface.addresses]
    for net in networks.values():
        subnet = net.subnet()
        matches = [ip for ip in all_ips if ipaddress.ip_address(ip) in subnet]
        if not matches:
            warnings.append(f"No local interface in expected subnet {net.name} ({subnet})")
    return warnings


def test_dns_resolution(hostnames: List[str]) -> List[str]:
    failures = []
    for host in hostnames:
        try:
            socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        except OSError as exc:
            failures.append(f"{host}: {exc}")
    return failures


def test_external_connectivity(host: str = "1.1.1.1", port: int = 443, timeout: float = 2.0) -> str | None:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return None
    except OSError as exc:
        return str(exc)


def summarize_routes() -> List[str]:
    return _run_ip_route()


def summarize_network(
    interfaces: List[InterfaceInfo],
    routes: List[str],
    dns_servers: List[str],
    subnet_warnings: List[str],
    dns_failures: List[str],
    ext_error: str | None,
) -> Dict[str, object]:
    return {
        "interfaces": [{"name": i.name, "addresses": i.addresses} for i in interfaces],
        "routes": routes,
        "dns_servers": dns_servers,
        "subnet_warnings": subnet_warnings,
        "dns_failures": dns_failures,
        "external_connectivity_error": ext_error,
    }
