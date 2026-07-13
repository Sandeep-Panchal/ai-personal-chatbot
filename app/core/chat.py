from app.core.memory import MemoryManager
from app.llm.ollama_call import OllamaClient
from app.services.title_service import TitleService
from typing import Generator

class ChatService:

    def __init__(self):

        self.memory = MemoryManager()
        self.ollama = OllamaClient()
        self.title_service = TitleService(self.ollama.client)

    def chat(
        self,
        session_id: str,
        user_message: str,
    ) -> Generator[str, None, None]:

        # Step 1 - Store user message
        self.memory.add_user_message(
            session_id=session_id,
            message=user_message,
        )

        # Step 2 - Get complete conversation history
        history = self.memory.get_session_history(session_id=session_id)

        # Step 3
        chunks = []
        for chunk in self.ollama.ollama_chat(history):
            chunks.append(chunk)
            yield chunk

        ai_message = "".join(chunks)

        # Step 4 - Store AI response
        self.memory.add_ai_message(
            session_id=session_id,
            message=ai_message.strip(),
        )

        # Step 5 - Create title if not created
        if self.memory.is_new_chat(session_id=session_id):
            history = self.memory.get_session_history(session_id)
            title = self.title_service.generate_title(history)

            self.memory.update_title(
                session_id=session_id,
                title=title,
            )
    
    def get_session_history(
            self,
            session_id: str
            ):
        
        return self.memory.get_session_history(session_id)

    def get_all_sessions(self):

        return self.memory.get_all_sessions()

if __name__ == "__main__":

    import json
    from app.core.session import SessionManager

    session = SessionManager()
    chat_obj = ChatService()

    session_id = session.create_session()

    print(f"Session ID: {session_id}")

    while True:

        user_message = input("You: ")

        if user_message.lower() == "new chat":
            session_id = session.create_session()
            print()
            print("*"*30)
            print("New chat session started...")
            print("*"*30, "\n")
            user_message = input("You: ")

        if user_message.lower() == "exit":
            break

        response = chat_obj.chat(
            session_id=session_id,
            user_message=user_message,
        )

        for chunk in response:
            print(chunk, end="", flush=True)
        print("-"*50)

    print("="*50)
    print("\nConversation History\n")
    print(chat_obj.memory.sessions)