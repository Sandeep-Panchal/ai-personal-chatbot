from app.llm.ollama_call import OllamaClient

from app.memory.session_memory import SessionMemory
from app.memory.message_memory import MessageMemory
from app.memory.summary_memory import SummaryMemory

from app.agents.title_agent import TitleAgent

from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage

from typing import Generator

class ChatService:

    def __init__(self):

        self.ollama = OllamaClient()
        self.session_memory = SessionMemory()
        self.message_memory = MessageMemory()
        self.summary_memory = SummaryMemory(self.ollama.client)
        self.title_agent = TitleAgent(self.ollama.client)

        self.default_title = "New Chat"

    def messages_input_formatting(self, messages_data: list[ChatMessage]) -> list[dict]:
        
        message_history = []
        for tup in messages_data:

            temp_dic = {}
            temp_dic["role"] = tup.role
            temp_dic["content"] = tup.message
            message_history.append(temp_dic)

        return message_history

    def chat(
        self,
        session_id: str,
        user_message: str,
    ) -> Generator[str, None, None]:

        # Step 1 - Store session
        self.session_memory.add_session(session_id=session_id)

        # Step 2 - Store user message
        self.message_memory.add_user_message(
            session_id=session_id,
            message=user_message,
        )

        # Step 3 - Get complete conversation history
        history = self.get_message_history(session_id)

        # Step 4
        chunks = []
        for chunk in self.ollama.ollama_chat(history):
            chunks.append(chunk)
            yield chunk

        ai_message = "".join(chunks)

        # Step 5 - Store AI response
        self.message_memory.add_ai_message(
            session_id=session_id,
            message=ai_message.strip(),
        )

        # Step 6 - Create title if not created
        session_data = self.get_session(session_id=session_id)
                    
        if session_data.title == self.default_title:
            history = self.get_message_history(session_id=session_id)

            title = self.title_agent.generate_title(history)

            self.session_memory.update_session_title(
                title=title,
                session_id=session_id
            )

        # Step 7 - call update summary to add summary periodically
        self.summary_memory.update_summary(session_id=session_id)
    
    def get_message_history(self, session_id: str) -> None:
        
        messages_data = self.message_memory.get_message_history(session_id)
        history = self.messages_input_formatting(messages_data=messages_data)
        return history
    
    def get_session(self, session_id: str) -> ChatSession | None:

        return self.session_memory.get_session_by_id(session_id=session_id)

    def get_all_sessions(self) -> list[ChatSession]:

        return self.session_memory.get_all_sessions()

if __name__ == "__main__":

    pass
    # from app.core.session import SessionManager

    # session = SessionManager()
    # chat_obj = ChatService()

    # session_id = session.create_session()

    # print(f"Session ID: {session_id}")

    # while True:

    #     user_message = input("You: ")

    #     if user_message.lower() == "new chat":
    #         session_id = session.create_session()
    #         print()
    #         print("*"*30)
    #         print("New chat session started...")
    #         print("*"*30, "\n")
    #         user_message = input("You: ")

    #     if user_message.lower() == "exit":
    #         break

    #     response = chat_obj.chat(
    #         session_id=session_id,
    #         user_message=user_message,
    #     )

    #     for chunk in response:
    #         print(chunk, end="", flush=True)
    #     print("-"*50)

    # # history = chat_obj.get_message_history(session_id)
    # # print(history)

    # # print(type(history))