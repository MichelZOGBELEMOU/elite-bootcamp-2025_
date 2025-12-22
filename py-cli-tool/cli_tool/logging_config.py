"""Logging configuration for the CLI tool"""

import logging


def get_logger(level: str) -> logging.Logger:
    """Return a configured application logger"""

    # Logger
    logger = logging.getLogger("py-cli-tool")
    logger.setLevel(level)
    logger.propagate = False

    return logger
