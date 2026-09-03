from src.app.graph.state import ChatbotState
from src.app.graph.nodes import *

from langgraph.graph import StateGraph, START, END

class GraphBuilder:

    def __init__(self):

        # Graph builder
        self.chatbot_graph = StateGraph(ChatbotState)

    def create_nodes(self):

        self.chatbot_graph.add_node("chat_node", chat_node)
        self.chatbot_graph.add_node("should_generate_title_node", should_generate_title_node)
        self.chatbot_graph.add_node("title_node", title_node)
        self.chatbot_graph.add_node("should_summarize_node", should_summarize_node)
        self.chatbot_graph.add_node("summary_node", summary_node)

    def create_edges(self):

        # Creating edges
        self.chatbot_graph.add_edge(START, "chat_node")
        self.chatbot_graph.add_edge("chat_node", "should_generate_title_node")

        self.chatbot_graph.add_conditional_edges(
            "should_generate_title_node",
            title_router,
            {
                "true": "title_node",
                "false": "should_summarize_node"
            }
        )

        self.chatbot_graph.add_conditional_edges(
            "should_summarize_node",
            summarize_router,
            {
                "true": "summary_node",
                "false": END
            }
        )

        self.chatbot_graph.add_edge("title_node", "should_summarize_node")
        self.chatbot_graph.add_edge("summary_node", END)

    def graph_builder(self):

        self.create_nodes()
        self.create_edges()

        # Compile the graph
        return self.chatbot_graph.compile()

if __name__=="__main__":

    graph_obj = GraphBuilder()

    graph_compile = graph_obj.graph_builder()
    
    result = graph_compile.stream({
            "session_id":"123",
            "user_message":"hi, how are you",
            "llm_response":""
        },
        stream_mode="custom"
        )

    print(result)

