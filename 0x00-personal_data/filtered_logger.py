#!/usr/bin/env python3
"""Filred logger module."""
from typing import List
import re
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """method to filter values in incoming log records using"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Function that returns the log message obfuscated"""
    for field in fields:
        obfuscated = re.sub(rf'{field}=.+?{separator}',
                            f'{field}={redaction}{separator}', message)
        message = obfuscated
    return message


def get_logger() -> logging.Logger:
    """function that takes no arguments and returns a logging.Logger object."""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(streamHandler)
    return logger
