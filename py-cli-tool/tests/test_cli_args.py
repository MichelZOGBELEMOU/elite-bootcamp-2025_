"""Tests for CLI argument handling and subcommand routing."""

import json
from pathlib import Path
import sys

import pytest

from cli_tool import cli
from cli_tool import env_detect
from cli_tool import vm_health


def _write_config(tmp_path: Path) -> Path:
    config = {
        "environment": {
            "name": "test-env",
            "domain": "test.local",
            "description": "test description",
        },
        "defaults": {"vm": {"os_family": "debian", "os_version": "12"}},
        "networks": {
            "lan": {"cidr": "10.10.0.0/24", "gateway": "10.10.0.1"},
        },
        "vms": [
            {
                "name": "host1",
                "hostname": "host1.test.local",
                "role": "control",
                "machine_type": "bare-metal",
                "os": {"family": "ubuntu", "version": "25.04"},
                "networks": [{"name": "lan", "ip": "10.10.0.10"}],
            }
        ],
    }
    cfg = tmp_path / "config.yaml"
    cfg.write_text(json.dumps(config), encoding="utf-8")
    return cfg


def test_env_command_outputs_expected_fields(monkeypatch, capsys, tmp_path):
    cfg = _write_config(tmp_path)
    monkeypatch.setattr(cli, "DEFAULT_CONFIG_PATH", cfg)
    monkeypatch.setattr(cli, "DEFAULT_LOG_FILE", tmp_path / "log.txt")

    monkeypatch.setattr(env_detect, "detect_os", lambda: env_detect.OSInfo("ubuntu", "25.04"))
    monkeypatch.setattr(
        env_detect,
        "detect_virtualization",
        lambda: env_detect.VirtualizationInfo(is_virtualized=False, type=None, hint=None),
    )

    monkeypatch.setattr(sys, "argv", ["prog", "env"])
    cli.run()
    out = capsys.readouterr().out
    assert "Environment: test-env" in out
    assert "Host OS: ubuntu 25.04" in out


def test_vms_command_uses_health_checks(monkeypatch, capsys, tmp_path):
    cfg = _write_config(tmp_path)
    monkeypatch.setattr(cli, "DEFAULT_CONFIG_PATH", cfg)
    monkeypatch.setattr(cli, "DEFAULT_LOG_FILE", tmp_path / "log.txt")

    def fake_check(vm):
        return vm_health.HealthStatus(name=vm.name, hostname=vm.hostname, status="healthy", reasons=["ok"])

    monkeypatch.setattr(vm_health, "check_vm", fake_check)
    monkeypatch.setattr(sys, "argv", ["prog", "vms", "--output", "json"])

    cli.run()
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["vms"][0]["name"] == "host1"
    assert data["vms"][0]["status"] == "healthy"


def test_config_error_causes_exit(monkeypatch, capsys, tmp_path):
    bad_cfg = tmp_path / "bad.yaml"
    bad_cfg.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(cli, "DEFAULT_CONFIG_PATH", bad_cfg)
    monkeypatch.setattr(cli, "DEFAULT_LOG_FILE", tmp_path / "log.txt")
    monkeypatch.setattr(sys, "argv", ["prog", "env"])

    with pytest.raises(SystemExit) as exc:
        cli.run()
    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "Configuration error" in err
