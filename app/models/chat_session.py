from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ChatSession:

    title: str = "New Chat"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    messages: list[dict] = field(default_factory=list)

if __name__=="__main__":

    session = ChatSession()
    print(session)