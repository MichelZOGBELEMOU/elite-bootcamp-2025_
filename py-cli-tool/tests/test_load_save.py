"""Test the load_save module"""

import logging
import pytest
from cli_tool import load_save as ls

LOGGER = logging.getLogger("test")
LOGGER.setLevel(logging.DEBUG)


def test_load_valid_yaml(tmp_path, caplog):
    """Test the case of a valid yaml file"""

    cfg = tmp_path / "config.yaml"
    yaml_text = "app:\n  port: 22\n"
    cfg.write_text(yaml_text, encoding="utf-8")
    caplog.set_level(logging.DEBUG)

    data = ls.load_yaml(cfg, LOGGER)

    assert isinstance(data, dict)
    assert data["app"]["port"] == 22
    assert any("successfully loaded" in r.message for r in caplog.records)
    assert any(r.levelname == "INFO" for r in caplog.records)


def test_load_yaml_file_not_found(tmp_path):
    """test the case where the YAML file do not exist"""
    cfg = tmp_path / "missing.yaml"

    with pytest.raises(FileNotFoundError):

        ls.load_yaml(cfg, LOGGER)


def test_load_yaml_raises_file_is_a_directory(tmp_path):
    """test the case the YAML file is a directory"""
    log_path = tmp_path / "DIR"
    log_path.mkdir(exist_ok=True)

    with pytest.raises(IsADirectoryError):
        ls.load_yaml(log_path, LOGGER)


def test_load_yaml_file_is_empty(tmp_path):
    """test the case the YAML file is empty"""

    cfg = tmp_path / "config.yaml"
    yaml_text = ""
    cfg.write_text(yaml_text, encoding="utf-8")

    with pytest.raises(ValueError):
        ls.load_yaml(cfg, LOGGER)


def test_load_yaml_raises_value_error(tmp_path):
    """test the case the root of the YAML file is not a dictionary"""

    cfg = tmp_path / "config.yaml"
    yaml_text = "- hosts\n - network\n"
    cfg.write_text(yaml_text, encoding="utf-8")

    with pytest.raises(ValueError):
        ls.load_yaml(cfg, LOGGER)
