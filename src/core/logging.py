import json
import logging.config
from datetime import datetime
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

    def formatMessage(self, record: logging.LogRecord) -> str:
        super().formatMessage(record)
        created_datetime: str = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        log_record = {
            "message": record.message,
            "level": record.levelname,
            "name": record.name,
            "path_name": record.pathname,
            "func_name": record.funcName,
            "line_number": record.lineno,
            "thread_id": record.thread,
            "datetime": created_datetime,
        }
        return json.dumps(log_record, ensure_ascii=False)


def setup_default_logging(is_dev_mode: bool = False) -> Dict[str, Any]:
    """Set up basic logging."""

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s()] %(message)s",
            },
            "json": {
                "()": lambda: JsonFormatter(),
            },
            "uvicorn_access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '[%(asctime)s] [%(process)s] [%(levelname)s] [%(name)s] %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "formatter": "default" if is_dev_mode else "json",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "uvicorn_access": {
                "formatter": "uvicorn_access",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "uvicorn.access": {
                "handlers": ["uvicorn_access"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(config)

    return config
