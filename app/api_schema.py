from pydantic import BaseModel, Field
from datetime import datetime

class ChatInputSchema(BaseModel):
    session_id: str = Field(min_length=1)
    query: str = Field(min_length=1)

class ChatOutputSchema(BaseModel):
    llm_response: str = Field(min_length=1)

class SessionIDSchema(BaseModel):
    session_id: str = Field(min_length=1)

class AllSessionSchema(BaseModel):
    session_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    created_at: datetime
    updated_at: datetime

class MessageHistorySchema(BaseModel):
    role: str
    content: str


if __name__=="__main__":

    obj = ChatInputSchema(query="sandeep")
    print(obj)