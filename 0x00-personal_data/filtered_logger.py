#!/usr/bin/env python3
""" filtered logger implementation """
from typing import List
import re
import logging


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self._fields, self.REDACTION, record.msg,
            self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """returns the log message obfuscated"""
    result = message
    for field in fields:
        result = re.sub(
            f"{field}=.*?{separator}",
            f"{field}={redaction}{separator}",
            result,
        )
    return result
