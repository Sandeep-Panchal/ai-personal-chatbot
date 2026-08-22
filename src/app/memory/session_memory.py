from src.app.database.repositories.session_repository import SessionRepository
from src.app.models.chat_session import ChatSession

from datetime import datetime

class SessionMemory:

    def __init__(self):
    
        self.session_repo = SessionRepository()
        self.default_title = "New Chat"

    def add_session(self, session_id: str) -> None:
    
        if self.session_repo.fetch_session_by_id(session_id) is None:
            created_at = updated_at = datetime.now()
            self.session_repo.insert_session(session_id, self.default_title, created_at, updated_at)

    def update_session_modified_time(self,
                                    session_id: str,
                                    updated_at: datetime
                                    ):
    
        self.session_repo.update_session_modified(session_id, updated_at)

    def get_session_by_id(self, session_id: str) -> ChatSession | None:
    
            return self.session_repo.fetch_session_by_id(session_id)

    def get_all_sessions(self) -> list[ChatSession]:
    
            return self.session_repo.fetch_all_sessions()

    def update_session_title(self,
                            title: str,
                            session_id: str
                            ) -> None:
        
        self.session_repo.update_session_title(title, session_id)

    def delete_session(self, session_id: str) -> None:

        self.session_repo.delete_session(session_id)

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