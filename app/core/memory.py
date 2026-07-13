class MemoryManager:

    def __init__(self):

        self.memory_dict = {
            "session_id": "",
            "messages": []
        }

    def add_user_message(
        self,
        session_id: str,
        message: str
    ) -> None:

        if not self.memory_dict["session_id"]:
            self.memory_dict["session_id"] = session_id

        self.memory_dict["messages"].append(
            {
                "role": "user",
                "content": message
            }
        )

    def add_ai_message(
        self,
        message: str
    ) -> None:

        self.memory_dict["messages"].append(
            {
                "role": "assistant",
                "content": message
            }
        )

    def get_history(self):

        return self.memory_dict["messages"]

    def clear_history(self):

        self.memory_dict = {
            "session_id": "",
            "messages": []
        }

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

        if user_message.lower() == "exit":
            break

        # Step 1
        memory.add_user_message(session_id, user_message)

        # Step 2
        history = memory.get_history()

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

    for message in memory.get_history():
        print(message)