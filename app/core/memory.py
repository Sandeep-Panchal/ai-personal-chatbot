from app.database.repositories.session_repository import SessionRepository
from app.database.repositories.message_repository import MessageRepository

from datetime import datetime

class MemoryManager:

    def __init__(self):

        self.session_repo = SessionRepository()
        self.message_repo = MessageRepository()

        self.default_title = "New Chat"

    def add_session(self, session_id: str) -> None:

        if self.session_repo.fetch_session_by_id(session_id) is None:
            
            created_at = datetime.now()
            updated_at = datetime.now()
            
            self.session_repo.insert_session(session_id, self.default_title, created_at, updated_at)

    def add_user_message(self,
                          session_id: str,
                          message: str,
                          role="user"
                        ) -> None:

        created_at = datetime.now()
        self.message_repo.insert_message(session_id, role, message, created_at)

    def add_ai_message(self,
                          session_id: str,
                          message: str,
                          role="assistant"
                        ) -> None:

        created_at = datetime.now()
        self.message_repo.insert_message(session_id, role, message, created_at)

    def get_message_history(self, session_id: str) -> list[tuple[int, str, str, str, str]]:
        
        messages_data = self.message_repo.fetch_messages_by_session_id(session_id)
        
        return messages_data
    
    def get_session(self, session_id: str) -> tuple[str, str, str, str] | None:

        return self.session_repo.fetch_session_by_id(session_id)
    
    def update_title(self,
                     title: str,
                     session_id: str
                    ) -> None:
        
        self.session_repo.update_session_title(title, session_id)

    
    # def get_all_sessions(self):

    #     return dict(
    #         sorted(
    #             self.sessions.items(),
    #             key=lambda item: item[1].created_at,
    #             reverse=False,
    #         )
    #     )
    
    # def is_new_chat(self, session_id: str) -> bool:

    #     return self.sessions[session_id].title == "New Chat"
    
    # def update_title(
    #         self,
    #         session_id: str,
    #         title: str,
    #     ):

    #     self.get_session(session_id).title = title

if __name__=="__main__":

    # from app.llm.ollama_call import OllamaClient
    from app.core.session import SessionManager

    memory = MemoryManager()
    session = SessionManager()
    # ollama_client = OllamaClient()

    # session_id = session.create_session()
    
    # n = 1
    # title = f"title_{n}"
    # created_at = f"created_{n}"
    # updated_at = f"updated_{n}"
    # memory.add_session(session_id, title, created_at, updated_at)

    session_id = "1"
    messages = memory.get_session_history(session_id)
    print(messages)