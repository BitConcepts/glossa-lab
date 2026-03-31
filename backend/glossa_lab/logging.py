"""Structured logging setup for Glossa Lab."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from pythonjsonlogger.json import JsonFormatter

if TYPE_CHECKING:
    from glossa_lab.config import Settings


def setup_logging(settings: Settings) -> None:
    """Configure structured JSON logging to console and file."""
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # JSON formatter
    formatter = JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"asctime": "timestamp", "levelname": "level", "name": "module"},
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # File handler — create log directory if needed
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "glossa.log"

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates on reload
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    logging.getLogger("glossa_lab").info(
        "Logging initialized",
        extra={"log_level": settings.log_level, "log_file": str(log_file)},
    )
