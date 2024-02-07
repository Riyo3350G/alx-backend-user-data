#!/usr/bin/env python3
"""Filred logger module."""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Function that returns the log message obfuscated"""
    for field in fields:
        obfuscated = re.sub(rf'{field}=.+?{separator}',
                            f'{field}={redaction}{separator}', message)
        message = obfuscated
    return message
