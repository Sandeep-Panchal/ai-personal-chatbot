from app.models.chat_session import ChatSession
from datetime import datetime

class MemoryManager:

    def __init__(self):

        self.sessions: dict[str, ChatSession] = {}

    def add_user_message(
        self,
        session_id: str,
        message: str
    ) -> None:

        if session_id not in self.sessions:
            self.sessions[session_id] = ChatSession()
            self.sessions[session_id].created_at = datetime.now()

        self.sessions[session_id].messages.append(
            {
                "role": "user",
                "content": message
            }
        )

        self.sessions[session_id].updated_at = datetime.now()

    def add_ai_message(
        self,
        session_id: str,
        message: str
    ) -> None:
        
        session = self.get_session(session_id)

        session.messages.append(
            {
                "role": "assistant",
                "content": message
            }
        )

        session.updated_at = datetime.now()

    def get_session(self, session_id: str) -> ChatSession:

        if session_id not in self.sessions:
            self.sessions[session_id] = ChatSession()

        return self.sessions[session_id]

    def get_session_history(self, session_id: str,):

        if session_id not in self.sessions:
            self.sessions[session_id] = ChatSession()

        return self.get_session(session_id).messages
        # return self.sessions[session_id].messages
    
    def get_all_sessions(self):

        return dict(
            sorted(
                self.sessions.items(),
                key=lambda item: item[1].updated_at,
                reverse=True,
            )
        )
    
    def is_new_chat(self, session_id: str) -> bool:

        return self.sessions[session_id].title == "New Chat"
    
    def update_title(
            self,
            session_id: str,
            title: str,
        ):

        self.get_session(session_id).title = title

if __name__=="__main__":

    from app.llm.ollama_call import OllamaClient
    from app.core.session import SessionManager

    memory = MemoryManager()
    session = SessionManager()
    ollama_client = OllamaClient()
    
    # for response in ollama_client.ollama_chat(settings.llm.example_query):
    #     print(response, end="", flush=True)

    session_id = session.create_session()
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

        # Step 1
        memory.add_user_message(session_id, user_message)

        # Step 2
        history = memory.get_session_history(session_id)

        # Step 3
        ai_message = "".join(
            ollama_client.ollama_chat(history)
        )

        print(f"Assistant: {ai_message}")

        # Step 4
        memory.add_ai_message(session_id, ai_message)
        print("-"*50)

    print("="*50)
    print("\nConversation History\n")

    print(memory.sessions)