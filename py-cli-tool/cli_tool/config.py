"""Configuration loading and validation for the homelab CLI tool."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional
import ipaddress
import yaml


class ConfigError(Exception):
    """Raised when the configuration file is invalid."""


@dataclass
class Environment:
    """General environment metadata."""

    name: str
    domain: str
    description: str


@dataclass
class Network:
    """Network definition."""

    name: str
    cidr: str
    gateway: str
    bridge: Optional[str] = None
    dns_servers: List[str] = field(default_factory=list)
    expected_hosts: Dict[str, str] = field(default_factory=dict)

    def subnet(self) -> ipaddress.IPv4Network:
        return ipaddress.ip_network(self.cidr, strict=False)


@dataclass
class VMNetwork:
    """Network attachment for a VM."""

    name: str
    ip: str


@dataclass
class VMChecks:
    """Health check options for a VM."""

    ping: bool = True
    ssh_port: int = 22
    uptime_check: bool = False


@dataclass
class VMDefinition:
    """VM or bare-metal host definition."""

    name: str
    hostname: str
    role: str
    os_family: str
    os_version: Optional[str]
    machine_type: str  # vm or bare-metal
    networks: List[VMNetwork]
    checks: VMChecks


@dataclass
class Defaults:
    """Defaults applied to VMs or networks when fields are missing."""

    vm_checks: VMChecks
    vm_os_family: Optional[str] = None
    vm_os_version: Optional[str] = None


@dataclass
class RootConfig:
    """Top-level configuration container."""

    environment: Environment
    networks: Dict[str, Network]
    vms: List[VMDefinition]
    defaults: Defaults


def _ensure_dict(data: Any, context: str) -> Mapping[str, Any]:
    if not isinstance(data, Mapping):
        raise ConfigError(f"{context} must be a mapping")
    return data


def _ensure_list(data: Any, context: str) -> Iterable[Any]:
    if not isinstance(data, list):
        raise ConfigError(f"{context} must be a list")
    return data


def _validate_ip(value: str, context: str) -> None:
    try:
        ipaddress.ip_address(value)
    except ValueError as exc:
        raise ConfigError(f"{context} must be a valid IP address: {exc}") from exc


def _validate_cidr(value: str, context: str) -> None:
    try:
        ipaddress.ip_network(value, strict=False)
    except ValueError as exc:
        raise ConfigError(f"{context} must be a valid CIDR: {exc}") from exc


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")
    if path.is_dir():
        raise ConfigError("Config path points to a directory, expected a file")
    content = path.read_text(encoding="utf-8")
    if not content.strip():
        raise ConfigError("Config file is empty")
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise ConfigError(f"Failed to parse YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError("Root of config must be a mapping")
    return data


def _parse_environment(raw: Mapping[str, Any]) -> Environment:
    required = ["name", "domain", "description"]
    for key in required:
        if key not in raw:
            raise ConfigError(f"environment.{key} is required")
        if not isinstance(raw[key], str):
            raise ConfigError(f"environment.{key} must be a string")
    return Environment(
        name=raw["name"],
        domain=raw["domain"],
        description=raw["description"],
    )


def _parse_networks(raw: Mapping[str, Any]) -> Dict[str, Network]:
    networks: Dict[str, Network] = {}
    for name, value in raw.items():
        node = _ensure_dict(value, f"networks.{name}")
        if "cidr" not in node or "gateway" not in node:
            raise ConfigError(f"networks.{name} requires cidr and gateway")
        cidr = node["cidr"]
        gateway = node["gateway"]
        if not isinstance(cidr, str):
            raise ConfigError(f"networks.{name}.cidr must be a string")
        if not isinstance(gateway, str):
            raise ConfigError(f"networks.{name}.gateway must be a string")
        _validate_cidr(cidr, f"networks.{name}.cidr")
        _validate_ip(gateway, f"networks.{name}.gateway")
        dns_servers = node.get("dns_servers", [])
        if not isinstance(dns_servers, list):
            raise ConfigError(f"networks.{name}.dns_servers must be a list")
        for idx, ip_val in enumerate(dns_servers):
            if not isinstance(ip_val, str):
                raise ConfigError(f"networks.{name}.dns_servers[{idx}] must be a string")
            _validate_ip(ip_val, f"networks.{name}.dns_servers[{idx}]")
        expected_hosts = node.get("expected_hosts", {})
        if not isinstance(expected_hosts, dict):
            raise ConfigError(f"networks.{name}.expected_hosts must be a mapping")
        for host, ip_val in expected_hosts.items():
            if not isinstance(ip_val, str):
                raise ConfigError(f"networks.{name}.expected_hosts.{host} must be a string")
            _validate_ip(ip_val, f"networks.{name}.expected_hosts.{host}")
        networks[name] = Network(
            name=name,
            cidr=cidr,
            gateway=gateway,
            bridge=node.get("bridge"),
            dns_servers=dns_servers,
            expected_hosts=expected_hosts,
        )
    if not networks:
        raise ConfigError("networks cannot be empty")
    return networks


def _parse_vm_networks(raw: Any, known_networks: Mapping[str, Network]) -> List[VMNetwork]:
    attachments: List[VMNetwork] = []
    for idx, net in enumerate(_ensure_list(raw, "vm.networks")):
        item = _ensure_dict(net, f"vm.networks[{idx}]")
        if "name" not in item or "ip" not in item:
            raise ConfigError(f"vm.networks[{idx}] requires name and ip")
        name = item["name"]
        ip = item["ip"]
        if name not in known_networks:
            raise ConfigError(f"vm.networks[{idx}].name references unknown network '{name}'")
        if not isinstance(ip, str):
            raise ConfigError(f"vm.networks[{idx}].ip must be a string")
        _validate_ip(ip, f"vm.networks[{idx}].ip")
        attachments.append(VMNetwork(name=name, ip=ip))
    if not attachments:
        raise ConfigError("vm.networks cannot be empty")
    return attachments


def _parse_vm_checks(raw: Any, defaults: VMChecks) -> VMChecks:
    if raw is None:
        ping = defaults.ping
        ssh_port = defaults.ssh_port
        uptime_check = defaults.uptime_check
    else:
        node = _ensure_dict(raw, "vm.checks")
        ping = node.get("ping", defaults.ping)
        ssh_port = node.get("ssh_port", defaults.ssh_port)
        uptime_check = node.get("uptime_check", defaults.uptime_check)
    if not isinstance(ping, bool):
        raise ConfigError("vm.checks.ping must be a boolean")
    if not isinstance(ssh_port, int):
        raise ConfigError("vm.checks.ssh_port must be an integer")
    if ssh_port <= 0 or ssh_port > 65535:
        raise ConfigError("vm.checks.ssh_port must be between 1 and 65535")
    if not isinstance(uptime_check, bool):
        raise ConfigError("vm.checks.uptime_check must be a boolean")
    return VMChecks(ping=ping, ssh_port=ssh_port, uptime_check=uptime_check)


def _parse_vms(
    raw: Any,
    known_networks: Mapping[str, Network],
    defaults: Defaults,
) -> List[VMDefinition]:
    vms: List[VMDefinition] = []
    for idx, item in enumerate(_ensure_list(raw, "vms")):
        node = _ensure_dict(item, f"vms[{idx}]")
        name = node.get("name")
        hostname = node.get("hostname")
        role = node.get("role")
        machine_type = node.get("machine_type", "vm")
        os_node = node.get("os", {})
        if not all(isinstance(val, str) for val in [name, hostname, role]):
            raise ConfigError(f"vms[{idx}] name, hostname, and role must be strings")
        if machine_type not in {"vm", "bare-metal"}:
            raise ConfigError(f"vms[{idx}].machine_type must be 'vm' or 'bare-metal'")
        os_family = os_node.get("family", defaults.vm_os_family)
        os_version = os_node.get("version", defaults.vm_os_version)
        if not os_family:
            raise ConfigError(f"vms[{idx}].os.family is required (or set defaults.vm.os_family)")
        if not isinstance(os_family, str):
            raise ConfigError(f"vms[{idx}].os.family must be a string")
        if os_version is not None and not isinstance(os_version, (str, int)):
            raise ConfigError(f"vms[{idx}].os.version must be string or int")
        vm_networks = _parse_vm_networks(node.get("networks", []), known_networks)
        checks = _parse_vm_checks(node.get("checks"), defaults.vm_checks)
        vms.append(
            VMDefinition(
                name=name,
                hostname=hostname,
                role=role,
                os_family=os_family,
                os_version=str(os_version) if os_version is not None else None,
                machine_type=machine_type,
                networks=vm_networks,
                checks=checks,
            )
        )
    if not vms:
        raise ConfigError("vms cannot be empty")
    return vms


def load_config(path: Path) -> RootConfig:
    """Load, validate, and normalize the YAML configuration."""

    data = _load_yaml(path)

    defaults_node = _ensure_dict(data.get("defaults", {}), "defaults")
    vm_defaults_node = _ensure_dict(defaults_node.get("vm", {}), "defaults.vm")
    vm_checks = VMChecks(
        ping=vm_defaults_node.get("ping", True),
        ssh_port=vm_defaults_node.get("ssh_port", 22),
        uptime_check=vm_defaults_node.get("uptime_check", False),
    )
    vm_os_family = vm_defaults_node.get("os_family")
    vm_os_version = vm_defaults_node.get("os_version")
    defaults = Defaults(vm_checks=vm_checks, vm_os_family=vm_os_family, vm_os_version=vm_os_version)

    env = _parse_environment(_ensure_dict(data.get("environment", {}), "environment"))
    networks = _parse_networks(_ensure_dict(data.get("networks", {}), "networks"))
    vms = _parse_vms(data.get("vms", []), networks, defaults)

    return RootConfig(environment=env, networks=networks, vms=vms, defaults=defaults)
