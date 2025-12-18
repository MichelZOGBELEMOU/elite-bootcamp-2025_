"""Module for managing loading and saving of YAML an JSON configuration files"""

from typing import Any
from pathlib import Path
import logging
import json
import yaml


def load_yaml(file: Path, logger: logging.Logger) -> dict[str, Any]:
    """Load and parse a YAML configuration file.

    Return:
        dict: Parsed YAML configuration
    exits:
        Non-zero if file cannot be loaded or is invalid
    """
    logger.debug(f"Loading YAML file '{file}'")

    if file.is_dir():
        raise IsADirectoryError("Cannot open a directory as a file.")

    if not file.exists():
        raise FileNotFoundError(f"Yaml file '{file}' not found.")

    with file.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if data is None:
        raise ValueError("YAML file is empty.")

    if not isinstance(data, dict):
        raise ValueError("YAML root element must be a dictionary.")

    logger.info(f"YAML '{file}' successfully loaded.")
    return data


def load_json(file: Path, logger: logging.Logger) -> dict[str, Any]:
    """
    Load and parse json configuration file
    """
    if file.is_dir():
        raise IsADirectoryError("Cannot open a directory as a file.")

    if not file.exists():
        raise FileNotFoundError(f"JSON file '{file}' not found.")

    with file.open(encoding="utf-8") as f:
        data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("JSON file root must be a dictionary")

        logger.info(f"JSON file '{file}' successfully loaded")
        return data


def convert_yaml_to_json(
    logger: logging.Logger, source: Path, destination: Path = Path("config.json")
) -> None:
    """Convert YAML file to JSON file"""
    destination.parent.mkdir(exist_ok=True)
    logger.debug(f"Converting {source} to {destination}")

    data = load_yaml(source, logger)

    with destination.open(mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)

        logger.info(f"YAML file '{source}' converted to JSON file '{destination}'")


def save_json(logger: logging.Logger, data: dict[str, Any], file: Path) -> None:
    """Save data in a JSON file."""

    file.parent.mkdir(exist_ok=True)
    logger.debug(f"Saving data in json file {file}")

    with file.open(encoding="utf-8", mode="w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)

        logger.info(f"Data succesfully save in JSON file '{file}'")
