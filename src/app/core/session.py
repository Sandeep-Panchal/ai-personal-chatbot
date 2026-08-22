import uuid
from src.app.memory.session_memory import SessionMemory

class SessionManager:

    def __init__(self):
        self.session_memory = SessionMemory()

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())

        # persisting session id into db
        self.session_memory.add_session(session_id=session_id)

        return session_id
    
if __name__=="__main__":

    session = SessionManager()
    print(session.create_session())