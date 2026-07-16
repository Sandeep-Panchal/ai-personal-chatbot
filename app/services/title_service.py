from app.config import settings

class TitleService:

    def __init__(self, ollama_client):

        self.ollama = ollama_client

    def generate_title(self, history: list[dict]) -> str:

        user = history[0]["content"]
        assistant = history[1]["content"]

        messages = [
                {
                    "role": "system",
                    "content": (
                        "You generate concise chat titles. "
                        "Return only the title. "
                        "Maximum 3 words."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Conversation:\n\n"
                        f"User: {user}\n\n"
                        f"Assistant: {assistant}"
                    ),
                },
            ]

        response = self.ollama.chat(
            model=settings.llm.model_name,
            messages=messages,
            stream=False,
        )

        return response["message"]["content"].strip()
    
if __name__=="__main__":

    from app.llm.ollama_call import OllamaClient
    ollama = OllamaClient()
    title_obj = TitleService(ollama.client)

    messages=[{'role': 'user', 'content': 'i want to learn langgraph'},
              {'role': 'assistant', 'content': "LangChain is a popular framework for developing applications with large language models (LLMs)."
              "It focuses on how to integrate LLMs like GPT-3, ChatGPT and others into your own projects."
              "\n\nDo you have any questions about LangChain specifically? I can help you understand it better if you'd like! "
              "Just let me know what interests you about LangChain."}]

    title = title_obj.generate_title(messages)
    print(f"Title: {title}")


    