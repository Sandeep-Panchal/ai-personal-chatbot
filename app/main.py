from fastapi import FastAPI

from app.core.chat import ChatService
from app.core.session import SessionManager
from app.api_schema import (
    ChatInputSchema,
    ChatOutputSchema,
    AllSessionSchema,
    MessageHistorySchema,
    SessionIDSchema
)

chat = ChatService()
session = SessionManager()

# Creating an instance of FastAPI
fapp = FastAPI()

@fapp.post("/api/chat", response_model=ChatOutputSchema)
def chat_api(data: ChatInputSchema):

    response = chat.chat(
        session_id=data.session_id,
        user_message=data.query,
        )
    response_text = "".join(response)

    return {"llm_response": response_text}

@fapp.post("/api/sessions", response_model=SessionIDSchema)
def create_session():
    session_id = session.create_session()
    return {"session_id": session_id}

@fapp.get("/api/sessions", response_model=list[AllSessionSchema])
def get_all_sessions():
    return chat.get_all_sessions()

@fapp.get("/api/sessions/{session_id}", response_model=AllSessionSchema)
def get_single_session(session_id: str):
    return chat.get_session(session_id)

@fapp.get("/api/sessions/{session_id}/messages", response_model=list[MessageHistorySchema])
def get_message_history(session_id: str):
    return chat.get_message_history(session_id)

@fapp.delete("/api/sessions/{session_id}")
def delete_session(session_id: str):
    chat.delete_chat(session_id)
    return {"message": "Session deleted successfully"}

if __name__=="__main__":
    pass