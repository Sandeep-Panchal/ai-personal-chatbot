from ollama import Client

class OllamaClient:

    def __init__(self):

        self.client = Client()

    def ollama_chat(self, model_name, query, stream=False):

        messages = [
            {
                'role': 'user',
                'content': query,
            },
        ]

        for part in self.client.chat(model_name, messages=messages, stream=stream):
            yield part['message']['content']

if __name__ == "__main__":

    ollama_client = OllamaClient()
    model_name = "llama3.1:8b"
    query = "Hello, how are you?"
    stream = True

    for response in ollama_client.ollama_chat(model_name, query, stream):
        print(response, end="", flush=True)
