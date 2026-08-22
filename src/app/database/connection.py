import sqlite3
from pathlib import Path

class DBConnection:

    def __init__(self):

        self.DATABASE_PATH = Path(__file__).parent / "db" / "chatbot_testing.db"

    def get_connection(self):
        
        connection = sqlite3.connect(self.DATABASE_PATH)
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection

if __name__=="__main__":
    pass 
