"""CLI entrypoint and subcommand routing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List

from dataclasses import replace

from cli_tool import env_detect, net_diag, vm_health
from cli_tool.config import ConfigError, RootConfig, VMChecks, load_config
from cli_tool.logging_config import DEFAULT_LOG_FILE, get_logger


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "-c",
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=f"Path to YAML config (default: {DEFAULT_CONFIG_PATH})",
    )
    common.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    common.add_argument(
        "-o",
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )

    parser = argparse.ArgumentParser(
        prog="homelab-cli",
        description="Homelab diagnostics and inventory tool",
        parents=[common],
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("env", help="Show environment and virtualization info", parents=[common])

    vms_parser = subparsers.add_parser("vms", help="Check VM health", parents=[common])
    vms_parser.add_argument(
        "--name",
        action="append",
        help="Limit checks to VMs by name (repeatable)",
    )
    vms_parser.add_argument(
        "--skip-ping",
        action="store_true",
        help="Skip ICMP ping checks",
    )
    vms_parser.add_argument(
        "--skip-ssh",
        action="store_true",
        help="Skip SSH port probe",
    )

    net_parser = subparsers.add_parser("net", help="Run network diagnostics", parents=[common])
    net_parser.add_argument(
        "--skip-dns",
        action="store_true",
        help="Skip DNS resolution tests",
    )
    net_parser.add_argument(
        "--external-host",
        default="1.1.1.1",
        help="External host to test connectivity",
    )
    net_parser.add_argument(
        "--external-port",
        type=int,
        default=443,
        help="External port to test connectivity",
    )

    return parser


def _load_configuration(path: Path) -> RootConfig:
    return load_config(path)


def handle_env(args: argparse.Namespace, config: RootConfig) -> dict[str, Any]:
    os_info = env_detect.detect_os()
    virt_info = env_detect.detect_virtualization()
    data = {
        "environment": {
            "name": config.environment.name,
            "domain": config.environment.domain,
            "description": config.environment.description,
        },
        "host": {
            "os_family": os_info.family,
            "os_version": os_info.version,
            "virtualized": virt_info.is_virtualized,
            "virtualization_type": virt_info.type,
            "hint": virt_info.hint,
        },
    }
    return data


def _filter_vms(config: RootConfig, names: List[str] | None) -> List:
    if not names:
        return config.vms
    wanted = {n.lower() for n in names}
    return [vm for vm in config.vms if vm.name.lower() in wanted]


def handle_vms(args: argparse.Namespace, config: RootConfig) -> dict[str, Any]:
    results = []
    for vm in _filter_vms(config, args.name):
        checks: VMChecks = vm.checks
        if args.skip_ping:
            checks = VMChecks(ping=False, ssh_port=checks.ssh_port, uptime_check=checks.uptime_check)
        if args.skip_ssh:
            checks = VMChecks(ping=checks.ping, ssh_port=0, uptime_check=checks.uptime_check)
        vm_copy = replace(vm, checks=checks)
        status = vm_health.check_vm(vm_copy)
        results.append(status.as_dict())
    return {"vms": results}


def handle_net(args: argparse.Namespace, config: RootConfig) -> dict[str, Any]:
    interfaces = net_diag.collect_interfaces()
    routes = net_diag.summarize_routes()
    dns_servers = net_diag.collect_dns_servers()
    subnet_warnings = net_diag.validate_subnets(interfaces, config.networks)
    dns_failures: List[str] = []
    if not args.skip_dns:
        hostnames = [config.environment.domain] + list(
            {host for net in config.networks.values() for host in net.expected_hosts.keys()}
        )
        dns_failures = net_diag.test_dns_resolution(hostnames)
    ext_error = net_diag.test_external_connectivity(args.external_host, args.external_port)
    return net_diag.summarize_network(
        interfaces=interfaces,
        routes=routes,
        dns_servers=dns_servers,
        subnet_warnings=subnet_warnings,
        dns_failures=dns_failures,
        ext_error=ext_error,
    )


def _print_text(data: dict[str, Any]) -> None:
    # Minimal text renderer for the structured outputs
    if "environment" in data and "host" in data:
        env = data["environment"]
        host = data["host"]
        print(f"Environment: {env['name']} ({env['domain']})")
        print(f"Description: {env['description']}")
        virt = "virtualized" if host["virtualized"] else "bare-metal"
        vtype = f" ({host['virtualization_type']})" if host.get("virtualization_type") else ""
        print(f"Host OS: {host['os_family']} {host['os_version']}, {virt}{vtype}")
        if host.get("hint"):
            print(f"Virtualization hint: {host['hint']}")
    if "vms" in data:
        for vm in data["vms"]:
            reasons = "; ".join(vm["reasons"])
            print(f"{vm['name']}: {vm['status']} - {reasons}")
    if "interfaces" in data:
        print("Interfaces:")
        for iface in data["interfaces"]:
            print(f"  {iface['name']}: {', '.join(iface['addresses']) or 'no addresses'}")
        if data.get("routes"):
            print("Routes:")
            for route in data["routes"]:
                print(f"  {route}")
        if data.get("dns_servers"):
            print(f"DNS servers: {', '.join(data['dns_servers'])}")
        if data.get("subnet_warnings"):
            print("Subnet warnings:")
            for warn in data["subnet_warnings"]:
                print(f"  - {warn}")
        if data.get("dns_failures"):
            print("DNS failures:")
            for fail in data["dns_failures"]:
                print(f"  - {fail}")
        if data.get("external_connectivity_error"):
            print(f"External connectivity error: {data['external_connectivity_error']}")
        else:
            print("External connectivity: ok")


def run(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    log_level = "DEBUG" if args.verbose else "INFO"
    logger = get_logger(log_level, log_file=DEFAULT_LOG_FILE)

    try:
        config = _load_configuration(args.config)
    except ConfigError as exc:
        logger.error("Configuration error: %s", exc)
        parser.exit(2, f"Configuration error: {exc}\n")

    if args.command == "env":
        data = handle_env(args, config)
    elif args.command == "vms":
        data = handle_vms(args, config)
    elif args.command == "net":
        data = handle_net(args, config)
    else:
        parser.error("Unknown command")

    if args.output == "json":
        print(json.dumps(data, indent=2))
    else:
        _print_text(data)
