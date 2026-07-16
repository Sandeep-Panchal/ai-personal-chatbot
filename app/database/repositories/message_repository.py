import sqlite3
from app.database.connection import DBConnection

class MessageRepository:

    def insert_message(self,
                        session_id: str,
                        role: str,
                        message: str,
                        created_at: str
                    ) -> bool:
        
        insert_message_query = """
            INSERT INTO messages (session_id, role, message, created_at)
            VALUES (?, ?, ?, ?);
        """

        try:

            connection = DBConnection().get_connection()
            cursor = connection.cursor()

            cursor.execute(
                insert_message_query,
                (session_id, role, message, created_at)
            )

            connection.commit()
            return True

        except sqlite3.Error:
            raise

        finally:
            connection.close()

    def get_messages_by_session_id(self, session_id: str)-> tuple[int, str, str, str, str]:

        messages_by_session_id_query = """
                SELECT * FROM messages
                WHERE session_id = ?
                ORDER BY message_id;
            """
        
        try:
            connection = DBConnection().get_connection()
            cursor = connection.cursor()

            cursor.execute(messages_by_session_id_query, (session_id,))
            row = cursor.fetchall()

            return row

        except sqlite3.Error:
            raise

        finally:
            connection.close()
        
    def get_all_messages(self)-> list[tuple[int, str, str, str, str]]:

        all_messages_query = """SELECT * FROM messages;"""
        
        try:
            connection = DBConnection().get_connection()
            cursor = connection.cursor()

            cursor.execute(all_messages_query)
            rows = cursor.fetchall()

            return rows

        except sqlite3.Error:
            raise

        finally:
            connection.close()


if __name__=="__main__":

    msg_repo = MessageRepository()
    
    num = 3
    
    # if msg_repo.insert_message(num, f"role_{num}", f"message_{num}", f"start_{num}"):
    #     print("Insertion successful")
    
    # row = msg_repo.get_messages_by_session_id("123")
    # print(row)

    row = msg_repo.get_messages_by_session_id("3")
    print(row)

    # rows = msg_repo.get_all_messages()
    # for row in rows:
    #     print(row)