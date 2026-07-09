import streamlit as st

from app.config import settings
from app.core.chat import ChatService

chat = ChatService()

st.title(f":blue[{settings.app.app_name}]")

with st.sidebar:
    if st.button("New Chat"):
        # create new session
        pass

user_message = st.chat_input("Say something")
if user_message:
    st.write(user_message)

    response = chat.invoke_llm(user_message)
    st.write_stream(response)