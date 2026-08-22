import sqlite3
from src.app.database.connection import DBConnection
from src.app.models.chat_message import ChatMessage
from src.config import settings

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

    def fetch_messages_by_session_id(self, session_id: str) -> list[ChatMessage]:

        messages_by_session_id_query = """
                SELECT * FROM messages
                WHERE session_id = ?
                ORDER BY message_id;
            """
        
        try:
            connection = DBConnection().get_connection()
            cursor = connection.cursor()

            cursor.execute(messages_by_session_id_query, (session_id,))
            rows = cursor.fetchall()

            messages = []

            for row in rows:
                messages.append(
                    ChatMessage(
                        message_id=row[0],
                        session_id=row[1],
                        role=row[2],
                        message=row[3],
                        created_at=row[4],
                    )
                )

            return messages

        except sqlite3.Error:
            raise

        finally:
            connection.close()

    def fetch_recent_messages(self, session_id: str) -> list[ChatMessage]:
    
            messages_by_session_id_query = """
                    SELECT * FROM messages
                    WHERE session_id = ?
                    ORDER BY message_id DESC
                    LIMIT ?;
                """
            
            try:
                connection = DBConnection().get_connection()
                cursor = connection.cursor()
    
                cursor.execute(messages_by_session_id_query, (session_id, settings.summary_settings.KEEP_LAST_MESSAGES))
                rows = cursor.fetchall()
                rows = rows.reverse()
    
                messages = []
    
                for row in rows:
                    messages.append(
                        ChatMessage(
                            message_id=row[0],
                            session_id=row[1],
                            role=row[2],
                            message=row[3],
                            created_at=row[4],
                        )
                    )
    
                return messages
    
            except sqlite3.Error:
                raise
    
            finally:
                connection.close()
        
    def fetch_all_messages(self) -> list[ChatMessage]:

        all_messages_query = """
                    SELECT * FROM messages
                    ORDER BY message_id;    
                """
        
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

    def fetch_messages_range(self,
                session_id: str,
                offset: int,
            ) -> list[ChatMessage]:
    
        message_range_query = """
                            SELECT *
                            FROM messages
                            WHERE session_id = ?
                            ORDER BY message_id
                            LIMIT ? OFFSET ?;  
                        """
        
        try:
            connection = DBConnection().get_connection()
            cursor = connection.cursor()

            count = settings.summary_settings.NEXT_MESSAGES_COUNT
            cursor.execute(message_range_query, (session_id, count, offset))
            rows = cursor.fetchall()

            messages = []
                
            for row in rows:
                messages.append(
                    ChatMessage(
                        message_id=row[0],
                        session_id=row[1],
                        role=row[2],
                        message=row[3],
                        created_at=row[4],
                    )
                )

            return messages

        except sqlite3.Error:
            raise

        finally:
            connection.close()

    def fetch_conversation_count(self, session_id: str) -> int | None:
    
        chat_count_query = """
                SELECT count(*) FROM messages
                WHERE session_id = ?;
            """
        
        try:
            connection = DBConnection().get_connection()
            cursor = connection.cursor()

            cursor.execute(chat_count_query, (session_id,))
            total_rows = cursor.fetchone()[0]

            return total_rows

        except sqlite3.Error:
            raise

        finally:
            connection.close()


if __name__=="__main__":

    msg_repo = MessageRepository()
    
    num = 3
    
    # if msg_repo.insert_message(1, f"role_{num}", f"message_{num}", f"start_{num}"):
    #     print("Insertion successful")
    
    # row = msg_repo.fetch_messages_by_session_id("1")
    # print(row)

    # lst = []
    # for r in row:
    #     temp_dic = {}
    #     temp_dic["role"] = r.role
    #     temp_dic["content"] = r.content
    #     lst.append(temp_dic)

    # print(lst)


    # row = msg_repo.fetch_messages_by_session_id("3")
    # print(row)

    # rows = msg_repo.fetch_all_messages()
    # for row in rows:
    #     print(row)

    session_id = "7a364242-a2a9-488f-a311-117d1b3c21c5"
    row = msg_repo.fetch_recent_messages(session_id)
    print(len(row))
    print(row)