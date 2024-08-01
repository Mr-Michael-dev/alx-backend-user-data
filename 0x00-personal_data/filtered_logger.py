#!/usr/bin/env python3
"""
contains a function called filter_datum that returns the log message obfuscated
"""
import re


def filter_datum(fields: list, redaction: str,
                 message: str, seperator: str) -> str:
    """Obfuscates a log message and return it"""
    for field in fields:
        pattern = fr'{field}=[^{seperator}]+'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message
