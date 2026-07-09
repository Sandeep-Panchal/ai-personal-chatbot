from ollama import Client
from app.config import settings

class OllamaClient:

    def __init__(self):

        self.client = Client()

    def ollama_chat(self, query):

        messages = [
            {
                'role': 'user',
                'content': query,
            },
        ]

        for part in self.client.chat(
            model=settings.llm.model_name,
            messages=messages,
            stream=settings.llm.stream
            ):

            yield part['message']['content']

if __name__ == "__main__":

    ollama_client = OllamaClient()
    
    for response in ollama_client.ollama_chat(settings.llm.example_query):

        print(response, end="", flush=True)
