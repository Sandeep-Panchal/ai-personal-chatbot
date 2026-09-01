from src.app.graph.graph import GraphBuilder


graph = GraphBuilder()
graph_compile = graph.graph_builder()

# mermaid = graph_compile.get_graph().draw_mermaid()

# with open("chatbot_graph.mmd", "w", encoding="utf-8") as file:
#     file.write(mermaid)

graph_image = graph_compile.get_graph().draw_mermaid_png()

with open("chatbot_graph.png", "wb") as file:
    file.write(graph_image)

# uv run python -m src.app.graph.visualize