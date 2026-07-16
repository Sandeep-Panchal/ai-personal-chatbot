import sqlite3
from app.database.connection import DBConnection

class SessionRepository:

    def insert_session(self,
                        session_id: str,
                        title: str,
                        created_at: str,
                        updated_at: str
                    )-> bool:

        insert_session_query = """
            INSERT INTO sessions (session_id, title, created_at, updated_at)
            VALUES (?, ?, ?, ?);
        """
        
        try:
            connection = DBConnection().get_connection()
            cursor = connection.cursor()

            cursor.execute(
                insert_session_query,
                (session_id, title, created_at, updated_at)
            )
            
            connection.commit()
            return True

        except sqlite3.Error:
            raise

        finally:
            connection.close()

    def fetch_session_by_id(self, session_id: str) -> tuple[str, str, str, str] | None:

        session_by_id_query = """
                SELECT * FROM sessions
                WHERE session_id = ?;
            """
        
        try:
            connection = DBConnection().get_connection()
            cursor = connection.cursor()

            cursor.execute(session_by_id_query, (session_id,))
            row = cursor.fetchone()

            return row

        except sqlite3.Error:
            raise

        finally:
            connection.close()
        
    def fetch_all_sessions(self)-> list[tuple[str, str, str, str]]:

        all_sessions_query = """SELECT * FROM sessions;"""
        
        try:
            connection = DBConnection().get_connection()
            cursor = connection.cursor()

            cursor.execute(all_sessions_query)
            rows = cursor.fetchall()

            return rows

        except sqlite3.Error:
            raise

        finally:
            connection.close()

    def update_session_title(self,
                             title: str,
                             session_id: str
                        ) -> bool:

        update_title_query = """
                    UPDATE sessions
                    SET title = ?
                    WHERE session_id = ?;
                """
        
        try:
            connection = DBConnection().get_connection()
            cursor = connection.cursor()

            cursor.execute(
                update_title_query, (title, session_id)
                )
            connection.commit()

            return True

        except sqlite3.Error:
            raise

        finally:
            connection.close()


if __name__=="__main__":

    ses_repo = SessionRepository()
    
    num = 2

    # row = ses_repo.fetch_session_ids()
    # print(row)
    
    # if ses_repo.insert_session(num, f"title_{num}", f"start_{num}", f"end_{num}"):
    #     print("Insertion successful")
    
    row = ses_repo.fetch_session_by_id("123")
    print(row)

    # row = ses_repo.fetch_session_by_id("3")
    # print(row)

    # rows = ses_repo.fetch_all_sessions()
    # for row in rows:
    #     print(row)