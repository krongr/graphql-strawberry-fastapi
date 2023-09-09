import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from settings import EVENT_LOG_FORMAT, ERROR_LOG_FORMAT, BACKUP_LOG_COUNT


class CustomLogger:

    def __init__(self):
        self.event_logger = self._create_event_logger()
        self.error_logger = self._create_error_logger()

    def _file_handler(
        self, fname: str, level: int, format: str
    ) -> TimedRotatingFileHandler:
        fname = Path('_logs') / f'{fname}.log'
        handler = TimedRotatingFileHandler(
            filename=fname,
            when='midnight',
            interval=1,
            backupCount=BACKUP_LOG_COUNT,
            encoding='utf-8',
            delay=True,
        )
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(format))
        return handler

    def _stdout_handler(
        self, level: int, format: str
    ) -> logging.StreamHandler:
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(format))
        return handler

    def _create_event_logger(self) -> logging.Logger:
        logger = logging.getLogger('event')
        logger.setLevel(logging.INFO)
        logger.addHandler(
            self._file_handler('event', logging.INFO, EVENT_LOG_FORMAT)
        )
        logger.addHandler(
            self._stdout_handler(logging.INFO, EVENT_LOG_FORMAT)
        )
        return logger

    def _create_error_logger(self) -> logging.Logger:
        logger = logging.getLogger('error')
        logger.setLevel(logging.ERROR)
        logger.addHandler(
            self._file_handler('error', logging.ERROR, ERROR_LOG_FORMAT)
        )
        return logger

    def log_event(self, msg: str):
        self.event_logger.info(msg)

    def log_warning(self, msg: str):
        self.event_logger.warning(msg)

    def log_error(self, msg: str):
        self.event_logger.error(msg)
        self.error_logger.exception(msg)
