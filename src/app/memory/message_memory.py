
from src.app.database.repositories.message_repository import MessageRepository
from src.app.memory.session_memory import SessionMemory
from src.app.models.chat_message import ChatMessage

from datetime import datetime

class MessageMemory:

    def __init__(self):

        self.message_repo = MessageRepository()

        self.session_memory = SessionMemory()

    def add_user_message(self,
                          session_id: str,
                          message: str,
                          role: str = "user"
                        ) -> None:

        timestamp = datetime.now()
        self.message_repo.insert_message(session_id, role, message, timestamp)

        self.session_memory.update_session_modified_time(session_id, timestamp)

    def add_ai_message(self,
                          session_id: str,
                          message: str,
                          role: str = "assistant"
                        ) -> None:

        timestamp = datetime.now()
        self.message_repo.insert_message(session_id, role, message, timestamp)

        self.session_memory.update_session_modified_time(session_id, timestamp)

    def get_message_history(self, session_id: str) -> list[ChatMessage]:
        
        messages_data = self.message_repo.fetch_messages_by_session_id(session_id)
        
        return messages_data
    
    
if __name__=="__main__":

    pass
    # # from app.llm.ollama_call import OllamaClient
    # from app.core.session import SessionManager

    # memory = MemoryManager()
    # session = SessionManager()
    # # ollama_client = OllamaClient()

    # # session_id = session.create_session()
    
    # # n = 1
    # # title = f"title_{n}"
    # # created_at = f"created_{n}"
    # # updated_at = f"updated_{n}"
    # # memory.add_session(session_id, title, created_at, updated_at)

    # session_id = "1"
    # messages = memory.get_session_history(session_id)
    # print(messages)