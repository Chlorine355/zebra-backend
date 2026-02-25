import logging
from logging.config import dictConfig
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": os.path.join(LOG_DIR, "app.log"),
            "maxBytes": 10_485_760, 
            "backupCount": 5,         
            "level": "INFO",
            "encoding": "utf-8",
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "loggers": {
        "zebra_backend": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    }
}

def setup_logging():
    dictConfig(LOGGING_CONFIG)
    logging.getLogger("zebra_backend").info("Logging started")