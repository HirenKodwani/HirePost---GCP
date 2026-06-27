from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from .config import LogLevel, settings


class LoggerFactory:
    _instances: dict[str, logging.Logger] = {}
    _initialized = False

    @classmethod
    def initialize(cls, log_dir: Optional[Path] = None) -> None:
        if cls._initialized:
            return
        cls._initialized = True

        log_dir = log_dir or settings.logs_dir
        log_dir.mkdir(parents=True, exist_ok=True)

        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, settings.log_level.value))

        formatter = logging.Formatter(settings.log_format)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        if settings.log_to_file:
            file_handler = RotatingFileHandler(
                filename=str(log_dir / "autovideofactory.log"),
                maxBytes=settings.log_max_bytes,
                backupCount=settings.log_backup_count,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

            error_handler = RotatingFileHandler(
                filename=str(log_dir / "error.log"),
                maxBytes=settings.log_max_bytes,
                backupCount=settings.log_backup_count,
                encoding="utf-8",
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            root_logger.addHandler(error_handler)

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        if not cls._initialized:
            cls.initialize()
        if name not in cls._instances:
            logger = logging.getLogger(name)
            cls._instances[name] = logger
        return cls._instances[name]

    @classmethod
    def get_child(cls, parent: str, child: str) -> logging.Logger:
        return cls.get_logger(f"{parent}.{child}")


def get_logger(name: str) -> logging.Logger:
    return LoggerFactory.get_logger(name)
