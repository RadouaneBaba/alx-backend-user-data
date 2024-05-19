#!/usr/bin/env python3
""" filtered logger implementation """
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the record"""
        record.msg = filter_datum(
            self._fields, self.REDACTION, record.msg, self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """PII logger implementation"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """database connection using env variables"""
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
    )


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


def main():
    """main funciton implementation"""
    cnx = get_db()
    cursor = cnx.cursor()

    query = "SELECT * FROM users;"
    cursor.execute(query)
    logger = get_logger()
    for row in cursor:
        logger.info(row)
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    main()
