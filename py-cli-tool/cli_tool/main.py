"""CLI tool entry point"""

from pathlib import Path
import logging
import sys
import argparse
import yaml
from cli_tool.logging_config import get_logger
import cli_tool.load_save as ls

# Configurations
LOG_DIR = Path.home() / Path("py-cli-tool")
LOG_FILE = LOG_DIR / "clitool.log"
FORMATER = logging.Formatter(
    "[%(asctime)s]: %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
CONFIG_FILE = Path("config.yaml")


def main() -> None:
    """Main entry point for CLI tool"""

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(description="Devops Homelab cli tool")

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="List of subcommands"
    )

    # Add subcommands
    info_subcommand = subparsers.add_parser("info", help="display Homelab information")

    # add options
    info_subcommand.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    # Set logging level
    logging_level = "DEBUG" if args.verbose else "INFO"

    # Initiate logger
    logger = get_logger(logging_level)
    handler = logging.FileHandler(LOG_FILE)
    handler.setLevel(logging_level)
    handler.setFormatter(FORMATER)
    if not logger.handlers:
        logger.addHandler(handler)

    try:
        config_data = ls.load_yaml(CONFIG_FILE, logger)
    except FileNotFoundError as e:
        logger.error("error: %s", e)
        sys.exit(2)
    except IsADirectoryError as e:
        logger.error("Error: %s", e)
        sys.exit(2)
    except ValueError as e:
        logger.error("Error: %s", e)
        sys.exit(2)
    except PermissionError as e:
        logger.error("Permission denied: %s ", e)
        sys.exit(2)
    except yaml.YAMLError as e:
        logger.error("Problem while parsing Yaml file: %s.", e)
        sys.exit(2)
    if "hosts" not in config_data:
        logger.error("Invalid configuration: missing 'hosts' key.")
        sys.exit(2)
    if not isinstance(config_data["hosts"], list):
        logger.error("'hosts' must be a list.")
        sys.exit(2)

    if args.command == "info":
        logger.info("Homelab CLI tool initialized")
        logger.info("Number of hosts: %d. ", len(config_data["hosts"]))

        if args.verbose:
            logger.debug("verbose mode enbled")


if __name__ == "__main__":
    main()
