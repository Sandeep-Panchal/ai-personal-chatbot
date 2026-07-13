from app.core.memory import MemoryManager
from app.llm.ollama_call import OllamaClient
from typing import Generator

class ChatService:

    def __init__(self):

        self.memory = MemoryManager()
        self.ollama = OllamaClient()

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
        history = self.memory.get_history()

        # Step 3 - Send history to LLM
        # ai_message = "".join(
        #     self.ollama.ollama_chat(history)
        # )

        # Step 3
        chunks = []
        for chunk in self.ollama.ollama_chat(history):
            chunks.append(chunk)
            yield chunk

        ai_message = "".join(chunks)

        # Step 4 - Store AI response
        self.memory.add_ai_message(
            message=ai_message.strip(),
        )

    def get_history(self):

        return self.memory.get_history()
    
if __name__ == "__main__":

    from app.core.session import SessionManager

    session = SessionManager()
    chat_obj = ChatService()

    session_id = session.create_session()

    print(f"Session ID: {session_id}")

    while True:

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

    for message in chat_obj.get_history():
        print(f"{message['role']:>10}: {message['content']}")