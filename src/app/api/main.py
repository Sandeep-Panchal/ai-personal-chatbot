from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json

from src.app.graph.graph import GraphBuilder
from src.app.database.init_db import DatabaseInitializer
from src.app.core.chat import ChatService
from src.app.core.session import SessionManager
from src.app.api.api_schema import (
    ChatInputSchema,
    AllSessionSchema,
    MessageHistorySchema,
    SessionIDSchema,
    ChatOutputSchema
)

# Creating an instance of FastAPI
fapp = FastAPI()

chat = ChatService()
session = SessionManager()
DatabaseInitializer().initialize_database()

@fapp.post("/api/chat", response_model=ChatOutputSchema)
def chat_api(data: ChatInputSchema):

    session_id = data.session_id

    if session_id is None:
        session_id = session.create_session()

    graph = GraphBuilder()
    graph_compile = graph.graph_builder()
    
    graph_response = graph_compile.invoke({
        "session_id":session_id,
        "user_message":data.query,
        "llm_response":""
    })

    print(f"graph response: {graph_response}")

    llm_response = graph_response["llm_response"]

    return {
        "session_id": session_id,
        "llm_response": llm_response,
    }


# @fapp.post(
#         "/api/chat",
#         response_class=StreamingResponse
#         )
# def chat_api(data: ChatInputSchema):

#     session_id = data.session_id

#     if session_id is None:
#         session_id = session.create_session()

#     def generate():

#         response = chat.chat(
#             session_id=session_id,
#             user_message=data.query,
#         )

#         for chunk in response:
#             yield json.dumps({
#                 "session_id": session_id,
#                 "llm_response": chunk
#                 }) + "\n"

#     return StreamingResponse(
#         generate(),
#         media_type="application/x-ndjson"
#     )

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