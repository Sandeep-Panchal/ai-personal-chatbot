from app.core.memory import MemoryManager
from app.llm.ollama_call import OllamaClient
from app.services.title_service import TitleService
from typing import Generator

class ChatService:

    def __init__(self):

        self.memory = MemoryManager()
        self.ollama = OllamaClient()
        self.title_service = TitleService(self.ollama.client)

        self.default_title = "New Chat"

    def messages_input_formatting(self, messages_data: tuple):

        message_history = []
        for tup in messages_data:

            temp_dic = {}
            temp_dic["role"] = tup[2]
            temp_dic["content"] = tup[3]
            message_history.append(temp_dic)

        return message_history

    def chat(
        self,
        session_id: str,
        user_message: str,
    ) -> Generator[str, None, None]:

        # Step 1 - Store session
        self.memory.add_session(session_id=session_id)

        # Step 2 - Store user message
        self.memory.add_user_message(
            session_id=session_id,
            message=user_message,
        )

        # Step 3 - Get complete conversation history
        messages_data = self.get_message_history(session_id=session_id)

        # Step 4 - Input message formatting as per LLM input acceptance
        history = self.messages_input_formatting(messages_data=messages_data)

        # Step 5
        chunks = []
        for chunk in self.ollama.ollama_chat(history):
            chunks.append(chunk)
            yield chunk

        ai_message = "".join(chunks)

        # Step 6 - Store AI response
        self.memory.add_ai_message(
            session_id=session_id,
            message=ai_message.strip(),
        )

        # Step 7 - Create title if not created
        session_data = self.memory.get_session(session_id=session_id)
        if session_data[1] == self.default_title:
            messages_data = self.get_message_history(session_id=session_id)
            history = self.messages_input_formatting(messages_data=messages_data)

            title = self.title_service.generate_title(history)

            self.memory.update_title(
                title=title,
                session_id=session_id
            )
    
    def get_message_history(self, session_id: str) -> None:
        
        return self.memory.get_message_history(session_id)

    def get_all_sessions(self):

        return self.memory.get_all_sessions()

if __name__ == "__main__":

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