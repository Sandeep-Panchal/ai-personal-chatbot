import sqlite3
from src.app.database.connection import DBConnection
from src.app.models.chat_summary import ChatSummary

class SummaryRepository:

    def insert_summary(self,
                        session_id: str,
                        summary_version: int,
                        messages_summary: str,
                        covers_until_message_id: int,
                        created_at: str
                    ) -> bool:
        
        insert_summary_query = """
            INSERT INTO summary (
                session_id, summary_version, messages_summary, covers_until_message_id, created_at
                )
            VALUES (?, ?, ?, ?, ?);
        """

        try:

            connection = DBConnection().get_connection()
            cursor = connection.cursor()

            cursor.execute(
                insert_summary_query,
                (session_id, summary_version, messages_summary, covers_until_message_id, created_at)
            )

            connection.commit()
            return True

        except sqlite3.Error:
            raise

        finally:
            connection.close()

    def fetch_last_summary_by_session_id(self, session_id: str) -> ChatSummary | None:
    
        all_summary_query = """
                    SELECT * FROM summary
                    WHERE session_id = ?
                    ORDER BY summary_id DESC
                    LIMIT 1   
                """
        
        try:
            connection = DBConnection().get_connection()
            cursor = connection.cursor()

            cursor.execute(all_summary_query, (session_id,))
            row = cursor.fetchone()

            if row is None:
                return None

            return ChatSummary(
                    summary_id=row[0],
                    session_id=row[1],
                    summary_version=row[2],
                    messages_summary=row[3],
                    covers_until_message_id=row[4],
                    created_at=row[5]
                )

        except sqlite3.Error:
            raise

        finally:
            connection.close()

if __name__=="__main__":

    summary_repo = SummaryRepository()
    
    num = 3
    
    # if msg_repo.insert_message(1, f"role_{num}", f"message_{num}", f"start_{num}"):
    #     print("Insertion successful")
    
    # row = summary_repo.fetch_all_summaries_by_session_id("1")
    # print(row)

    # lst = []
    # for r in row:
    #     temp_dic = {}
    #     temp_dic["summary_id"] = r.summary_id
    #     temp_dic["session_id"] = r.session_id
    #     temp_dic["messages_summary"] = r.messages_summary
    #     lst.append(temp_dic)

    # print(lst)

    # row = msg_repo.fetch_messages_by_session_id("3")
    # print(row)

    # rows = msg_repo.fetch_all_messages()
    # for row in rows:
    #     print(row)

    rows_count = summary_repo.fetch_conversation_count(session_id="hhh")
    print(rows_count)