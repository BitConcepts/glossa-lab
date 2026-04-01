"""Structured logging setup for Glossa Lab."""

from __future__ import annotations

import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import TYPE_CHECKING

from pythonjsonlogger.json import JsonFormatter

if TYPE_CHECKING:
    from glossa_lab.config import Settings


def setup_logging(settings: Settings) -> None:
    """Configure structured JSON logging to console and file.

    File handler uses daily rotation, retaining 7 days of logs.
    """
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # JSON formatter
    formatter = JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"asctime": "timestamp", "levelname": "level", "name": "module"},
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # File handler with daily rotation, keep 7 days
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "glossa.log"

    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
        utc=True,
    )
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
