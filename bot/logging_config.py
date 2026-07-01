"""
logging_config.py
------------------
Sets up logging so that everything the bot does (requests, responses,
errors) gets written to a log file AND shown on screen.

Beginner note: "logging" is just a fancy, safer version of print().
Instead of print(), we use logger.info(), logger.error(), etc.
This automatically adds timestamps and saves everything to a file.
"""

import logging
import os

# Folder where log files will be saved
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "trading_bot.log")


def setup_logger():
    """
    Creates and returns a logger object that:
    - Writes logs to logs/trading_bot.log
    - Also prints logs to the terminal
    """
    # Make sure the logs folder exists
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers if this function is called twice
    if logger.handlers:
        return logger

    # Format: 2026-07-01 10:00:00 | INFO | message
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # 1. File handler -> writes logs to a file
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    # 2. Console handler -> prints logs to your terminal too
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
