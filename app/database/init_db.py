import sqlite3
from app.database.connection import DBConnection
from app.database.schema import (
    sessions_schema,
    messages_schema,
)

class DatabaseInitializer:

    def __init__(self):
        
        self.db = DBConnection()
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()

    def create_tables(self):

        self.cursor.execute(sessions_schema)
        self.cursor.execute(messages_schema)

    def initialize_database(self):

        try:
            self.create_tables()

            self.connection.commit()
            print("Database initialized successfully.")
        
        except sqlite3.Error as e:
            print(f"Database initialization failed: {e}")
        
        finally:
            self.connection.close()

if __name__ == "__main__":
    DatabaseInitializer().initialize_database()