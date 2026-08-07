# This file contains database schema for all the tables

#  Schema for session table
sessions_schema = """
    CREATE TABLE IF NOT EXISTS sessions
        (
            session_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
    """

# Schema for messages table
messages_schema = """
    CREATE TABLE IF NOT EXISTS messages
        (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,

            FOREIGN KEY (session_id)
                REFERENCES sessions(session_id)
        );
    """

# Schema for summary table
summary_schema = """
        CREATE TABLE IF NOT EXISTS summary
        (
            summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            summary_version INTEGER NOT NULL,
            messages_summary TEXT NOT NULL,
            covers_until_message_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            
            FOREIGN KEY(session_id)
                REFERENCES sessions(session_id)
    );
        """