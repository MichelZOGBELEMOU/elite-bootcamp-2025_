"""Logging configuration for the CLI tool."""

from __future__ import annotations

import logging
from pathlib import Path

DEFAULT_LOG_DIR = Path.home() / ".py-cli-tool"
DEFAULT_LOG_FILE = DEFAULT_LOG_DIR / "clitool.log"
LOG_FORMAT = "[%(asctime)s] %(levelname)s %(name)s - %(message)s"


def get_logger(level: str = "INFO", log_file: Path | None = None) -> logging.Logger:
    """Return a configured application logger with console and file handlers."""

    logger = logging.getLogger("py-cli-tool")
    logger.setLevel(level)
    logger.propagate = False

    log_path = log_file or DEFAULT_LOG_FILE
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")

    # Ensure handlers are added only once
    if not logger.handlers:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        for handler in logger.handlers:
            handler.setLevel(level)
            handler.setFormatter(formatter)

    return logger
