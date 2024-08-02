#!/usr/bin/env python3
"""
Contains a function called filter_datum that returns
the log message obfuscated
"""
import logging
import re


def filter_datum(fields: list,
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Obfuscates a log message and return it"""
    pattern = fr'({"|".join(fields)})=[^{separator}]+'
    return re.sub(pattern, lambda m: f'{m.group(1)}={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        formats a log record data using the filter_datum method
        """
        message = record.getMessage()
        record.msg = filter_datum(self.fields,
                                  self.REDACTION,
                                  message,
                                  self.SEPARATOR)

        return super(RedactingFormatter, self).format(record)
