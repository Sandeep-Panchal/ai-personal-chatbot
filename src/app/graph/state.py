from typing_extensions import TypedDict

class ChatbotState(TypedDict):

    session_id: str
    user_message: str
    llm_response: str
    should_generate_title: bool
    title: str
    summary: str
