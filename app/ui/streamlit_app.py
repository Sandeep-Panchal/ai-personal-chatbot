# import streamlit as st

# from app.config import settings
# from app.core.chat import ChatService

# chat = ChatService()

# st.title(f":blue[{settings.app.page_title}]")

# with st.sidebar:
#     if st.button("New Chat"):
#         # create new session
#         pass

# user_message = st.chat_input("Say something")
# if user_message:
#     st.write(user_message)

#     response = chat.invoke_llm(user_message)
#     st.write_stream(response)


import streamlit as st

from app.config import settings
from app.core.chat import ChatService
from app.core.session import SessionManager

st.title(f":blue[{settings.app.page_title}]")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = SessionManager().create_session()
if "conversation_ended" not in st.session_state:
    st.session_state.conversation_ended = False
if "chat_service" not in st.session_state:
    st.session_state.chat_service = ChatService()
if 'messages' not in st.session_state:
    st.session_state.messages = []

# with st.sidebar:
#     if st.button("New Chat"):
#         # create new session
#         pass

# user_message = st.chat_input("Say something")
# if user_message:
#     st.write(user_message)

#     response = chat.invoke_llm(user_message)
#     st.write_stream(response)

# Main content area - ONLY CONVERSATION AND RESULTS
st.subheader("💬 Chat")

# Display conversation
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                # st.markdown(message["content"])
                st.markdown(f"**You:** {message['content']}")
        else:
            with st.chat_message("assistant"):
                # st.markdown(message["content"])
                st.markdown(f"**Assistant:** {message['content']}")
    
    if st.session_state.conversation_ended:
        with st.chat_message("assistant"):
            st.info("Conversation Ended!")

# Chat input (only show if conversation is active)
if not st.session_state.conversation_ended:
    if prompt := st.chat_input("👤 Write down your query..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(f"**You:** {prompt}")
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 **Thinking...**"):
                response = st.session_state.chat_service.invoke_llm(prompt)
                st.write_stream(response)
                
                # Display AI response
                st.markdown(f"**Assistant:** {response}")
                
                # Add AI response to messages
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # # Handle conversation end
                # if conversation_ended :
                #     st.session_state.conversation_ended = True
                #     st.session_state.full_chat = full_chat
                #     print("st.session_state.full_chat", st.session_state.full_chat)
                #     st.rerun()