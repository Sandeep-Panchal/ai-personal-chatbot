import streamlit as st

from app.config import settings
from app.core.chat import ChatService
from app.core.session import SessionManager

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title=settings.app.page_title,
    page_icon="🤖",
    layout="wide",
)

st.title(f"🤖 {settings.app.page_title}")

# -------------------------------------------------------
# Initialize Session State
# -------------------------------------------------------

if "chat_service" not in st.session_state:
    st.session_state.chat_service = ChatService()

if "session_manager" not in st.session_state:
    st.session_state.session_manager = SessionManager()

if "session_id" not in st.session_state:
    st.session_state.session_id = (
        st.session_state.session_manager.create_session()
    )

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    st.header("💬 Chats")

    if st.button("➕ New Chat", use_container_width=True):

        st.session_state.session_id = (
            st.session_state.session_manager.create_session()
        )

        # Phase 1: recreate ChatService
        # Later this won't be needed when MemoryManager supports multiple sessions.
        st.session_state.chat_service = ChatService()

        st.rerun()

# -------------------------------------------------------
# Display Chat History
# -------------------------------------------------------

history = st.session_state.chat_service.get_history()

for message in history:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------------------------------
# Chat Input
# -------------------------------------------------------

if prompt := st.chat_input("Message AI Personal ChatBot..."):

    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream assistant response
    with st.chat_message("assistant"):

        st.write_stream(

            st.session_state.chat_service.chat(
                session_id=st.session_state.session_id,
                user_message=prompt,
            )

        )

    # # Refresh UI so saved history is displayed
    # st.rerun()