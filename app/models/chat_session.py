from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChatSession:
    session_id: str
    title: str
    created_at: datetime
    updated_at: datetime

if __name__=="__main__":

    session = ChatSession()
    print(session)
