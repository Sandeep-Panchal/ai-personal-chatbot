import uuid

class SessionManager:

    def create_session(self) -> str:
        return str(uuid.uuid4())
    
if __name__=="__main__":

    session = SessionManager()
    print(session.create_session())