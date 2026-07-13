from ollama import Client
from app.config import settings

from pathlib import Path

def load_system_prompt() -> str:
    prompt_path = (
        Path(__file__).parent.parent
        / "prompts"
        / "chat_system.txt"
    )

    return prompt_path.read_text(encoding="utf-8").strip()

class OllamaClient:

    def __init__(self):

        self.client = Client()

    def ollama_chat(self, messages):

        system_prompt = load_system_prompt()

        llm_messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        llm_messages.extend(messages)

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
