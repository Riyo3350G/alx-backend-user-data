#!/usr/bin/env python3
"""Filred logger module."""
from typing import List
import re
import logging
import os
import mysql.connector


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """function that returns a connector to the database"""
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )


def main():
    """The Main function"""
    database = get_db()
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]
    logger = get_logger()
    for row in cursor:
        msg = ''.join(f'{fld}={str(rw)}; ' for rw, fld in zip(row, fields))
        logger.info(msg)

    cursor.close()
    database.close()


if __name__ == "__main__":
    main()
