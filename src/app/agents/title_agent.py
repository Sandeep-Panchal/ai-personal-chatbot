from src.config import settings
from src.app.core.chat import ChatService
from src.app.utils.prompt_loading import PromptLoading
from src.app.memory.session_memory import SessionMemory
from src.app.llm.ollama_call import OllamaClient

class TitleAgent:

    def __init__(self):

        self.ollama = OllamaClient()
        self.prompt_loader = PromptLoading()
        self.chat = ChatService()
        self.session_memory = SessionMemory()

        self.default_title = "New Chat"

    def should_generate_title(self, session_id: str):

        session_data = self.session_memory.get_session_by_id(session_id=session_id)

        if session_data.title == self.default_title:
            return True
        return False

    def generate_title(self, session_id: str) -> None:

        history = self.chat.get_message_history(session_id=session_id)

        prompt_template = self.prompt_loader.load_prompt(
                self.prompt_loader.TITLE_PROMPT
                )

        user = history[0]["content"]
        assistant = history[1]["content"]

        prompt = prompt_template.format(
            user=user,
            assistant=assistant
        )

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
                    "content": prompt,
                },
            ]

        response = self.ollama.client.chat(
            model=settings.llm.model_name,
            messages=messages,
            stream=False,
        )

        updated_title = response["message"]["content"].strip()
        self.session_memory.update_session_title(
                        title=updated_title,
                        session_id=session_id
                    )

        return updated_title

if __name__=="__main__":

    from app.llm.ollama_call import OllamaClient
    ollama = OllamaClient()
    title_obj = TitleAgent(ollama.client)

    messages=[{'role': 'user', 'content': 'i want to learn langgraph'},
              {'role': 'assistant', 'content': "LangChain is a popular framework for developing applications with large language models (LLMs)."
              "It focuses on how to integrate LLMs like GPT-3, ChatGPT and others into your own projects."
              "\n\nDo you have any questions about LangChain specifically? I can help you understand it better if you'd like! "
              "Just let me know what interests you about LangChain."}]

    title = title_obj.generate_title(messages)
    print(f"Title: {title}")


    