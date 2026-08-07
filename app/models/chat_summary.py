from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChatSummary:
    summary_id: int
    session_id: str
    summary_version: str
    messages_summary: datetime
    covers_until_message_id: int
    created_at: datetime

if __name__=="__main__":

    summary = ChatSummary()
    print(summary)