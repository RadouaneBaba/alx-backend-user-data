#!/usr/bin/env python3
""" filtered logger implementation """
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    result = message
    for field in fields:
        result = re.sub(f"{field}=.*?{separator}", f"{field}={redaction}{separator}", result)
    return result
