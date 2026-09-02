from src.app.graph.state import ChatbotState
from src.app.core.chat import ChatService
from src.app.agents.title_agent import TitleAgent
from src.app.memory.summary_memory import SummaryMemory

chat = ChatService()
title_agent = TitleAgent()
summary_memory = SummaryMemory()

# Creating node functions
def chat_node(state: ChatbotState):

    response = chat.chat(
                session_id = state["session_id"],
                user_message = state["user_message"]
            )

    llm_response = "".join(response)

    return {
        "llm_response" : llm_response
    }

def should_generate_title_node(state: ChatbotState):
    bool = title_agent.should_generate_title(session_id=state["session_id"])
    return {
        "should_generate_title": bool
    }

def title_router(state: ChatbotState):
    if state["should_generate_title"]:
        return "true"
    return "false"

def title_node(state: ChatbotState):
    updated_title = title_agent.generate_title(session_id=state["session_id"])
    return {
        "title": updated_title
    }

def should_summarize_node(state: ChatbotState):
    bool, _ = summary_memory.should_summarize(session_id=state["session_id"])
    return {
        "should_summarize": bool
    }

def summarize_router(state: ChatbotState):
    if state["should_summarize"]:
        return "true"
    return "false"

def summary_node(state: ChatbotState):
    summary = summary_memory.update_summary(session_id=state["session_id"])
    return {
        "summary": summary
    }

    

    

    