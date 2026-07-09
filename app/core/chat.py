from app.llm.ollama_call import OllamaClient

ollama_client = OllamaClient()

class ChatService:

    def __init__(self):
        pass

    def invoke_llm(self, user_message: str):

        return ollama_client.ollama_chat(user_message)
    
if __name__=="__main__":

    chat = ChatService()

    user_message = "Hello, how are you?"
    
    for response in chat.invoke_llm(user_message):
        print(response, end="", flush=True)