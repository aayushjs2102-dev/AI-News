"""
Centralized logging configuration.
"""

import sys
from pathlib import Path

from loguru import logger


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Remove Loguru's default handler
logger.remove()

# Console logging
logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    enqueue=True
)

# General application log
logger.add(
    LOG_DIR / "app.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True
)

# Error log
logger.add(
    LOG_DIR / "error.log",
    level="ERROR",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True
)


def get_logger():
    """
    Return the configured Loguru logger.
    """
    return logger