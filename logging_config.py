import logging
from logging.handlers import RotatingFileHandler
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = "logs"

def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        f"{LOG_DIR}/bot.log",
        maxBytes=5_000_000,
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logging.basicConfig(
        level=LOG_LEVEL,
        handlers=[file_handler, console_handler],
    )

    logging.getLogger("telegram").setLevel(logging.WARNING)
    logging.getLogger("googleapiclient").setLevel(logging.WARNING)