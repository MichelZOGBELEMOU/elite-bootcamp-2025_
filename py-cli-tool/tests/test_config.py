"""Tests for configuration loading and validation."""

from pathlib import Path

import pytest

from cli_tool.config import ConfigError, load_config


def test_load_valid_config(tmp_path: Path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
environment:
  name: homelab
  domain: lab.local
  description: test env
defaults:
  vm:
    os_family: debian
    os_version: "12"
    ping: true
    ssh_port: 22
networks:
  lan:
    cidr: 10.10.0.0/24
    gateway: 10.10.0.1
vms:
  - name: node1
    hostname: node1.lab.local
    role: control
    machine_type: bare-metal
    os:
      family: ubuntu
      version: "25.04"
    networks:
      - name: lan
        ip: 10.10.0.10
""",
        encoding="utf-8",
    )

    config = load_config(cfg)
    assert config.environment.name == "homelab"
    assert config.networks["lan"].gateway == "10.10.0.1"
    assert config.vms[0].machine_type == "bare-metal"


def test_missing_network_raises(tmp_path: Path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
environment:
  name: homelab
  domain: lab.local
  description: test env
vms: []
""",
        encoding="utf-8",
    )
    with pytest.raises(ConfigError):
        load_config(cfg)


def test_invalid_ip_in_network(tmp_path: Path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
environment:
  name: homelab
  domain: lab.local
  description: test env
defaults:
  vm:
    os_family: debian
networks:
  lan:
    cidr: 10.10.0.0/24
    gateway: not-an-ip
vms:
  - name: node1
    hostname: node1.lab.local
    role: control
    machine_type: vm
    networks:
      - name: lan
        ip: 10.10.0.10
""",
        encoding="utf-8",
    )
    with pytest.raises(ConfigError):
        load_config(cfg)
