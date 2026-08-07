from app.config import settings
from app.utils.prompt_loading import PromptLoading
from app.models.chat_message import ChatMessage

class SummaryAgent:

    def __init__(self, ollama_client):

        self.ollama = ollama_client
        self.prompt_loader = PromptLoading()

        self.summary_prompt = self.prompt_loader.load_prompt(
                                self.prompt_loader.SUMMARY_PROMPT
                            )
    
    def conversation_to_text(self, conversation: list[ChatMessage]) -> str:

        return "\n".join(
            f"{i.role}: {i.message}"
            for i in conversation
        )

    def generate_summary(self,
                        new_conversation: list[ChatMessage],
                        previous_summary: str | None = None,
                        ) -> str:

        conversation_text = self.conversation_to_text(new_conversation)

        previous_summary = previous_summary or "<NO_PREVIOUS_SUMMARY>"

        prompt = self.summary_prompt.format(
            previous_summary=previous_summary,
            new_conversation=conversation_text
            )

        messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a conversation memory summarization assistant. "
                        "Follow the user's instructions exactly. "
                        "Return only the summary."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
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
    sum_obj = SummaryAgent(ollama.client)

    # prompt_template = sum_obj.load_summary_prompt()

    # print(prompt_template.format(previous_summary="aaa", conversation="bbb"))

    # resp = sum_obj.generate_summary_for(34, 24)
    # print(f"Bool: {resp[0]}, start_sum: {resp[1]}, end_sum: {resp[2]}")

    # messages=[{'role': 'user', 'content': 'i want to learn langgraph'},
    #               {'role': 'assistant', 'content': "LangChain is a popular framework for developing applications with large language models (LLMs)."
    #               "It focuses on how to integrate LLMs like GPT-3, ChatGPT and others into your own projects."
    #               "\n\nDo you have any questions about LangChain specifically? I can help you understand it better if you'd like! "
    #               "Just let me know what interests you about LangChain."}]

    # resp = sum_obj.generate_summary(messages)
    # print(resp)

    