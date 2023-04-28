#!/usr/bin/env python3
""" PII Module """

import csv
import logging
import os
import re
import mysql.connector
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Returns log message obfuscated """
    pattern = fr'({"|".join(fields)})=[^{separator}]+'
    return re.sub(pattern, f'\\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Init function """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formatter; filters values in incoming log records using filter_datum
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Function that takes no arguments and returns a logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    # Prevent propagation of log messages to other loggers
    logger.propagate = False

    # Create & add stream handler to logger
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the database
    (mysql.connector.connection.MySQLConnection object)
    """
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    connection = mysql.connector.connect(
        user=user, password=password, host=host, database=database
    )
    return connection


def main():
    """
    This function that takes no arguments and returns nothing.
    It obtains a db connection using get_db & retrieve all rows in the users
    table and display each row under a specific filtered format.
    """
    logger = get_logger()

    # Connect to the database and retrieve all rows in the users table
    cnx = get_db()
    cursor = cnx.cursor()
    query = "SELECT * FROM users;"
    cursor.execute(query)
    rows = cursor.column_names

    # Display each row under a filtered format
    for row in cursor:
        message = "".join([f"{rows}={str[row]}" for rows in row])
        logger.info(message.strip())

    # Close the database connection
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    main()
