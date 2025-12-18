"""Logging configuration for the CLI tool"""

import logging
from pathlib import Path

# Configurations
LOG_DIR = Path("/var/log/py-cli-tool")
LOG_FILE = LOG_DIR / "clitool.log"
FORMATER = logging.Formatter(
    "[%(asctime)s]: %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


def get_logger(level: str) -> logging.Logger:
    """Return a configured application logger"""

    # Creation of Logging folder
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Logger
    logger = logging.getLogger("py-cli-tool")
    logger.setLevel(level)
    logger.propagate = False

    # Handler
    if not logger.handlers:

        handler = logging.FileHandler(LOG_FILE)
        handler.setFormatter(FORMATER)
        handler.setLevel(level)
        logger.addHandler(handler)

    return logger
