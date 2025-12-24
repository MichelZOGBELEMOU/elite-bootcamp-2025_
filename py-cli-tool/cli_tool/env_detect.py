"""Environment detection utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import platform


@dataclass
class OSInfo:
    family: str
    version: str


@dataclass
class VirtualizationInfo:
    is_virtualized: bool
    type: str | None
    hint: str | None = None


def detect_os() -> OSInfo:
    """Detect OS family and version using /etc/os-release when available."""
    os_release = Path("/etc/os-release")
    family = platform.system()
    version = platform.release()
    if os_release.exists():
        data = {}
        for line in os_release.read_text(encoding="utf-8").splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip().strip('"')
        family = data.get("ID", family)
        version = data.get("VERSION_ID", version)
    return OSInfo(family=family, version=version)


def _read_dmi_field(name: str) -> str | None:
    path = Path("/sys/devices/virtual/dmi/id") / name
    try:
        return path.read_text(encoding="utf-8").strip()
    except (FileNotFoundError, PermissionError, OSError):
        return None


def detect_virtualization() -> VirtualizationInfo:
    """Detect virtualization hints from systemd-detect-virt, DMI, and cpuinfo."""
    systemd_type = _run_systemd_detect_virt()
    if systemd_type and systemd_type != "none":
        return VirtualizationInfo(is_virtualized=True, type=systemd_type)

    product_name = _read_dmi_field("product_name") or ""
    sys_vendor = _read_dmi_field("sys_vendor") or ""
    dmi_hint = f"{product_name} {sys_vendor}".strip() or None
    cpuinfo = Path("/proc/cpuinfo").read_text(encoding="utf-8")
    has_hypervisor = "hypervisor" in cpuinfo

    known = ["KVM", "QEMU", "VMware", "VirtualBox", "Bochs", "RHEV", "OpenStack", "Proxmox"]
    vm_type = None
    for name in known:
        if name.lower() in (product_name + sys_vendor).lower():
            vm_type = name.lower()
            break
    return VirtualizationInfo(
        is_virtualized=has_hypervisor or bool(vm_type),
        type=vm_type,
        hint=dmi_hint,
    )


def _run_systemd_detect_virt() -> str | None:
    try:
        result = subprocess.run(
            ["systemd-detect-virt", "--quiet", "--json=short"],
            check=False,
            capture_output=True,
            text=True,
            timeout=2,
        )
        if result.returncode == 0 and result.stdout:
            # Expecting a simple JSON string like "kvm"
            return result.stdout.strip().strip('"')
        if result.returncode == 1:
            return "none"
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        return None
    return None

