from app.llm.ollama_call import OllamaClient
import streamlit as st

ollama_client = OllamaClient()

st.title(":blue[AI Personal ChatBot]")

with st.sidebar:
    if st.button("New Chat"):
        # create new session
        pass

prompt = st.chat_input("Say something")
if prompt:
    st.write(prompt)

    model_name = "llama3.1:8b"
    stream = True

    response = ollama_client.ollama_chat(model_name, prompt, stream)
    st.write_stream(response)