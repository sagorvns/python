"""Logging utilities for Ciffly Chatbot."""
import logging
import os
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

def get_logger(name: str, level: str | None = None) -> logging.Logger:
    """Return a configured logger with optional file handler."""
    log = logging.getLogger(name)
    if log.handlers:
        return log
    log.setLevel(level or os.getenv("LOG_LEVEL", "INFO"))
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    # Console
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    log.addHandler(ch)
    # File
    fh = logging.FileHandler(LOG_DIR / "chatbot.log", encoding="utf-8")
    fh.setFormatter(fmt)
    log.addHandler(fh)
    return log

logger = get_logger(__name__)
