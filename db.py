import os

import psycopg2

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise RuntimeError("Set the DATABASE_URL environment variable.")

        self.connection = psycopg2.connect(database_url)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        try:
            self.connect()
            connection = self.connection
            cursor = self.cursor
            if connection is None or cursor is None:
                raise RuntimeError("Database connection was not established.")
            cursor.execute(query, params)
            connection.commit()
        except Exception:
            if self.connection:
                self.connection.rollback()
            raise
        finally:
            self.close()

    def fetch_results(self, query, params=None):
        try:
            self.connect()
            cursor = self.cursor
            if cursor is None:
                raise RuntimeError("Database cursor was not created.")
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception:
            if self.connection:
                self.connection.rollback()
            raise
        finally:
            self.close()

    def close(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            self.connection.close()
            self.connection = None
