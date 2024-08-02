#!/usr/bin/env python3
"""
Contains a function called filter_datum that returns the log message obfuscated.
"""
import re

def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
    """Obfuscates a log message and return it"""
    pattern = fr'({"|".join(fields)})=[^{separator}]+'
    return re.sub(pattern, lambda m: f'{m.group(1)}={redaction}', message)
