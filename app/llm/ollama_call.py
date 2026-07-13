from ollama import Client
from app.config import settings
from app.utils.prompt_loading import PromptLoading

class OllamaClient:

    def __init__(self):

        self.client = Client()
        self.prompt_loader = PromptLoading()

    def ollama_chat(self, history):

        self.system_prompt = self.prompt_loader.load_prompt(
            self.prompt_loader.SYSTEM_PROMPT
            )

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]

        messages.extend(history)

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
