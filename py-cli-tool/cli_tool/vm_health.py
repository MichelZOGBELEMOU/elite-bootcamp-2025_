"""VM health checking utilities."""

from __future__ import annotations

import socket
import subprocess
from dataclasses import dataclass
from typing import List, Tuple

from cli_tool.config import VMDefinition


@dataclass
class HealthStatus:
    name: str
    hostname: str
    status: str
    reasons: List[str]

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "hostname": self.hostname,
            "status": self.status,
            "reasons": self.reasons,
        }


def _ping(ip: str, timeout: int = 2) -> Tuple[bool, str | None]:
    cmd = ["ping", "-c", "1", "-W", str(timeout), ip]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 1)
    except FileNotFoundError:
        return False, "ping command not available"
    except subprocess.TimeoutExpired:
        return False, "ping timed out"
    if result.returncode == 0:
        return True, None
    return False, result.stderr.strip() or "ping failed"


def _probe_tcp(ip: str, port: int, timeout: int = 2) -> Tuple[bool, str | None]:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True, None
    except OSError as exc:
        return False, str(exc)


def check_vm(vm: VMDefinition, timeout: int = 2) -> HealthStatus:
    """Run connectivity checks for a VM or host."""
    reasons: List[str] = []
    status = "healthy"

    # Use first IP for reachability checks
    primary_ip = vm.networks[0].ip if vm.networks else None
    if vm.checks.ping and primary_ip:
        ok, err = _ping(primary_ip, timeout)
        if not ok:
            status = "degraded"
            reasons.append(f"ping failed: {err}")

    if vm.checks.ssh_port and primary_ip:
        ok, err = _probe_tcp(primary_ip, vm.checks.ssh_port, timeout)
        if not ok:
            status = "degraded"
            reasons.append(f"ssh port {vm.checks.ssh_port} unreachable: {err}")

    if vm.checks.uptime_check:
        # Placeholder: without credentials we cannot check uptime
        reasons.append("uptime_check requested but no credential mechanism implemented")
        if status == "healthy":
            status = "degraded"

    if status == "healthy" and not reasons:
        reasons.append("all checks passed")

    return HealthStatus(
        name=vm.name,
        hostname=vm.hostname,
        status=status,
        reasons=reasons,
    )

