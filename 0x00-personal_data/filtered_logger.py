#!/usr/bin/env python3
"""
Contains a function called filter_datum that returns
the log message obfuscated.
"""
import logging
import re
from typing import List
import os
import mysql.connector
from mysql.connector import connection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Obfuscates a log message and returns it.

    Args:
        fields (List[str]): List of fields to obfuscate.
        redaction (str): String to replace field values.
        message (str): Log message to be obfuscated.
        separator (str): Character separating fields in the log message.

    Returns:
        str: Obfuscated log message.
    """
    pattern = fr'({"|".join(fields)})=[^{separator}]+'
    return re.sub(pattern, lambda m: f'{m.group(1)}={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class.
    This class inherits from logging.Formatter and is used to obfuscate
    sensitive information in log messages.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter.

        Args:
            fields (List[str]): List of fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record's data using the filter_datum method.

        Args:
            record (logging.LogRecord): Log record to be formatted.

        Returns:
            str: Formatted and obfuscated log message.
        """
        message = record.getMessage()
        record.msg = filter_datum(self.fields,
                                  self.REDACTION,
                                  message,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a connector to the MySQL database using
    credentials from environment variables.

    Environment Variables:
        PERSONAL_DATA_DB_USERNAME: Username for the database (default: "root").
        PERSONAL_DATA_DB_PASSWORD: Password for the database (default: "").
        PERSONAL_DATA_DB_HOST: Hostname for the database
        PERSONAL_DATA_DB_NAME: Name of the database.

    Returns:
        MySQLConnection: A MySQLConnection object.
    """
    # Get database credentials from environment variables with defaults
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # Connect to the database
    conn = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return conn
