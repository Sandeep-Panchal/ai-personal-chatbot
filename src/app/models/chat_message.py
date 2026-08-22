from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChatMessage:
    message_id: int
    session_id: str
    role: str
    message: str
    created_at: datetime

if __name__=="__main__":

    message = ChatMessage()
    print(message)