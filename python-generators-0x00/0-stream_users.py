#!/usr/bin/python3
import mysql.connector
from seed import connect_to_prodev

def stream_users():
    """
    Generator that streams rows from the user_data table one by one.
    Yields each row as a dictionary.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    # Single loop generator using fetchone()
    row = cursor.fetchone()
    while row:
        yield row
        row = cursor.fetchone()

    cursor.close()
    connection.close()
