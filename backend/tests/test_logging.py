"""Tests for logging setup (TEST-LOG-001)."""

import json
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from glossa_lab.config import Settings
from glossa_lab.logging import setup_logging


def test_log_file_created(tmp_path: Path):
    """Log file is created in the specified directory."""
    settings = Settings(log_dir=tmp_path, log_level="DEBUG")
    setup_logging(settings)

    log_file = tmp_path / "glossa.log"
    assert log_file.exists()


def test_structured_json_output(tmp_path: Path):
    """Log output is valid JSON with required fields."""
    settings = Settings(log_dir=tmp_path, log_level="DEBUG")
    setup_logging(settings)

    test_logger = logging.getLogger("glossa_lab.test_structured")
    test_logger.info("test message")

    log_file = tmp_path / "glossa.log"
    lines = log_file.read_text(encoding="utf-8").strip().splitlines()
    # Find the test message
    found = False
    for line in lines:
        entry = json.loads(line)
        assert "timestamp" in entry
        assert "level" in entry
        assert "module" in entry
        assert "message" in entry
        if entry["message"] == "test message":
            found = True
    assert found


def test_file_handler_is_timed_rotating(tmp_path: Path):
    """File handler uses TimedRotatingFileHandler for daily rotation."""
    settings = Settings(log_dir=tmp_path, log_level="DEBUG")
    setup_logging(settings)

    root = logging.getLogger()
    rotating_handlers = [
        h for h in root.handlers if isinstance(h, TimedRotatingFileHandler)
    ]
    assert len(rotating_handlers) == 1
    handler = rotating_handlers[0]
    assert handler.when == "MIDNIGHT"
    assert handler.backupCount == 7
