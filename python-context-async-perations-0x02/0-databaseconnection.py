#!/usr/bin/env python3
import sqlite3


class DatabaseConnection:
    """Custom class-based context manager for SQLite connection"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # provide connection to the with-block

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            # Rollback if exception occurred, else commit
            if exc_type is not None:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()


if __name__ == "__main__":
    # Using the custom context manager to fetch users
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
