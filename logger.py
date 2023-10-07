"""
logger.py

This module defines a custom logging class `CustomLogger` tailored for
creating and handling both event and error logs. 

Key Features:
- Event Logger: Records all types of messages, from informational
  to warning and error messages.
- Error Logger: Specifically designed to record error messages along
  with their full tracebacks for deeper analysis and debugging.

Other functionalities include:
- Log events and errors with distinct formatting and handlers.
- Rotate log files based on a set interval to manage log size and
  backups.
- Ensure the existence of the logging directory and
  handle potential issues during log file creation.
- Offer streamlined logging methods for easier integration into
  applications.

Note:
    Ensure that the appropriate permissions and configurations
    are set for the logging directory and files when
    deploying in production environments.
"""


import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from settings import EVENT_LOG_FORMAT, ERROR_LOG_FORMAT, BACKUP_LOG_COUNT


class CustomLogger:
    """
    Custom Logger class for creating and handling event and error logs.

    Attributes:
        event_logger (Logger): Logger instance for events.
        error_logger (Logger): Logger instance for errors.

    Usage example:
        logger = CustomLogger('module_name')
        logger.log_event('This is an event message.')
        logger.log_error('This is an error message.')
    """

    def __init__(self, name: str):
        self.event_logger = self._create_event_logger()
        self.error_logger = self._create_error_logger(name)

    def _file_handler(
        self, fname: str, level: int, format: str
    ) -> TimedRotatingFileHandler:
        """
        Create a file handler for logging. This method ensures that the
        logging directory ('logs') exists, creating it if necessary.

        :param fname: Filename for the log.
        :param level: Logging level (e.g., logging.INFO, 40).
        :param format: Logging format.

        :return: Handler instance for logging into file.
        """
        if not os.path.exists('logs'):
            os.makedirs('logs')

        fname = Path('logs') / f'{fname}.log'
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
        """
        Create a stream handler for logging to stdout.

        :param level: Logging level.
        :param format: Logging format.

        :return: Handler instance for logging to stdout.
        """
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(format))
        return handler

    def _create_event_logger(self) -> logging.Logger:
        """
        Create and set up an event logger.

        :return: Configured logger for events.

        :raise OSError: Raised when there's an issue creating the file.
        """
        logger = logging.getLogger('event')
        logger.setLevel(logging.INFO)
        if not any(
            isinstance(h, logging.StreamHandler) for h in logger.handlers
        ):
            logger.addHandler(
                self._stdout_handler(logging.INFO, EVENT_LOG_FORMAT)
            )
        if not any(
            isinstance(h, TimedRotatingFileHandler) for h in logger.handlers
        ):
            try:
                logger.addHandler(
                    self._file_handler(
                        'event', logging.INFO, EVENT_LOG_FORMAT
                    )
                )
            except OSError:
                raise
        return logger

    def _create_error_logger(self, name: str) -> logging.Logger:
        """
        Create and set up an error logger with a given name.

        :param name: Name of the logger (e.g., module name).

        :return: Configured logger for errors.

        :raise OSError: Raised when there's an issue creating the file.
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.ERROR)
        if not any(
            isinstance(h, TimedRotatingFileHandler) for h in logger.handlers
        ):
            try:
                logger.addHandler(
                    self._file_handler(
                        'error', logging.ERROR, ERROR_LOG_FORMAT
                    )
                )
            except OSError:
                raise
        return logger

    def log_event(self, msg: str):
        """
        Log an event message.

        :param msg: Message to log.
        """
        self.event_logger.info(msg)

    def log_warning(self, msg: str):
        """
        Log a warning message.

        :param msg: Message to log.
        """
        self.event_logger.warning(msg)

    def log_error(self, msg: str):
        """
        Log an error message and exception stacktrace.

        :param msg: Message to log.
        """
        self.event_logger.error(msg)
        self.error_logger.exception(msg)
