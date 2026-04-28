"""Structured logging setup for Glossa Lab."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import TYPE_CHECKING

from pythonjsonlogger.json import JsonFormatter

if TYPE_CHECKING:
    from glossa_lab.config import Settings

# Third-party loggers that flood at DEBUG — cap them at WARNING regardless of
# the global log level.  aiosqlite logs every single execute/fetchone call,
# generating thousands of lines per hour at DEBUG.
_QUIET_LOGGERS = [
    "aiosqlite",
    "asyncio",
    "httpx",
    "httpcore",
    "hpack",
    "uvicorn.access",  # HTTP access log is emitted by uvicorn itself
]

# Size-based rotation limits
_MAX_BYTES = 10 * 1024 * 1024  # 10 MB per file
_BACKUP_COUNT = 5  # keep 5 rotated files → ≤55 MB total


def setup_logging(settings: Settings) -> None:
    """Configure structured JSON logging to console and file.

    File handler uses *size-based* rotation (10 MB / 5 backups → max ~55 MB).
    Noisy third-party loggers (aiosqlite, asyncio, httpx …) are capped at
    WARNING regardless of the global level so they never flood the log.
    """
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # JSON formatter
    formatter = JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"asctime": "timestamp", "levelname": "level", "name": "module"},
    )

    # Console handler — honour configured level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # File handler — size-based rotation: 10 MB × 5 files = ≤55 MB total
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "glossa.log"

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=_MAX_BYTES,
        backupCount=_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates on reload
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Silence third-party loggers that spam DEBUG entries
    for _name in _QUIET_LOGGERS:
        logging.getLogger(_name).setLevel(logging.WARNING)

    logging.getLogger("glossa_lab").info(
        "Logging initialized",
        extra={"log_level": settings.log_level, "log_file": str(log_file)},
    )
