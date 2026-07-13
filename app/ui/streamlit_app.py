# import streamlit as st

# from app.config import settings
# from app.core.chat import ChatService
# from app.core.session import SessionManager

# # -------------------------------------------------------
# # Page Configuration
# # -------------------------------------------------------

# st.set_page_config(
#     page_title=settings.app.page_title,
#     page_icon="🤖",
#     layout="wide",
# )

# st.title(f"🤖 {settings.app.page_title}")

# # -------------------------------------------------------
# # Initialize Session State
# # -------------------------------------------------------

# if "chat_service" not in st.session_state:
#     st.session_state.chat_service = ChatService()

# if "session_manager" not in st.session_state:
#     st.session_state.session_manager = SessionManager()

# if "session_id" not in st.session_state:
#     st.session_state.session_id = (
#         st.session_state.session_manager.create_session()
#     )

# # -------------------------------------------------------
# # Sidebar
# # -------------------------------------------------------

# with st.sidebar:

#     st.header("💬 Chats")

#     if st.button("➕ New Chat", use_container_width=True):

#         st.session_state.session_id = (
#             st.session_state.session_manager.create_session()
#         )

#         # Phase 1: recreate ChatService
#         # Later this won't be needed when MemoryManager supports multiple sessions.
#         st.session_state.chat_service = ChatService()

#         st.rerun()

# # -------------------------------------------------------
# # Display Chat History
# # -------------------------------------------------------

# history = st.session_state.chat_service.get_session_history()

# for message in history:

#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # -------------------------------------------------------
# # Chat Input
# # -------------------------------------------------------

# if prompt := st.chat_input("Message AI Personal ChatBot..."):

#     # Show user message immediately
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Stream assistant response
#     with st.chat_message("assistant"):

#         st.write_stream(

#             st.session_state.chat_service.chat(
#                 session_id=st.session_state.session_id,
#                 user_message=prompt,
#             )

#         )

#     # # Refresh UI so saved history is displayed
#     # st.rerun()

############################################################

import streamlit as st

from app.config import settings
from app.core.chat import ChatService
from app.core.session import SessionManager

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title=settings.app.page_title,
    page_icon="🤖",
    layout="wide",
)

# -------------------------------------------------------
# Session State
# -------------------------------------------------------

if "chat_service" not in st.session_state:
    st.session_state.chat_service = ChatService()

if "session_manager" not in st.session_state:
    st.session_state.session_manager = SessionManager()

if "session_id" not in st.session_state:
    st.session_state.session_id = (
        st.session_state.session_manager.create_session()
    )

chat = st.session_state.chat_service

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    st.title("🤖 AI ChatBot")

    st.caption("Personal AI Assistant")

    st.divider()

    if st.button(
        "➕ New Chat",
        use_container_width=True,
        type="primary",
    ):

        st.session_state.session_id = (
            st.session_state.session_manager.create_session()
        )

        st.rerun()

    st.divider()

    st.subheader("💬 Conversations")

    sessions = chat.get_all_sessions()

    if sessions:

        for session_id, session in sessions.items():

            active = session_id == st.session_state.session_id

            button_label = (
                f"🟢 {session.title}"
                if active
                else f"💬 {session.title}"
            )

            if st.button(
                button_label,
                key=session_id,
                use_container_width=True,
            ):

                st.session_state.session_id = session_id
                st.rerun()

    else:

        st.info("No conversations yet.")

    st.divider()

    st.subheader("⚙️ Model")

    st.code(settings.llm.model_name)

# -------------------------------------------------------
# Header
# -------------------------------------------------------

with st.container(border=True):

    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown("## 🤖 AI Personal ChatBot")

        st.caption(
            "Local AI Assistant powered by Ollama"
        )

    with col2:

        st.metric(
            "Model",
            settings.llm.model_name,
        )

# -------------------------------------------------------
# Current Chat Title
# -------------------------------------------------------

sessions = chat.get_all_sessions()

current_session = sessions.get(
    st.session_state.session_id
)

if current_session:

    with st.container(border=True):

        st.markdown(
            f"### 📄 {current_session.title}"
        )

        st.caption(
            f"Last updated : {current_session.updated_at.strftime('%d %b %Y • %I:%M %p')}"
        )

# -------------------------------------------------------
# Conversation
# -------------------------------------------------------

history = chat.get_session_history(
    st.session_state.session_id
)

with st.container(border=True):

    if not history:

        st.markdown("## 👋 Welcome")

        st.write(
            "Start a conversation with your AI assistant."
        )

        st.info(
            """
Try asking:

• Explain LangGraph

• Help me learn Python

• Summarize a document

• Plan my learning roadmap
"""
        )

    else:

        for message in history:

            avatar = (
                "👨‍💻"
                if message["role"] == "user"
                else "🤖"
            )

            with st.chat_message(
                message["role"],
                avatar=avatar,
            ):

                st.markdown(
                    message["content"]
                )

# -------------------------------------------------------
# Chat Input
# -------------------------------------------------------

if prompt := st.chat_input(
    "Ask me anything..."
):

    with st.chat_message(
        "user",
        avatar="👨‍💻",
    ):

        st.markdown(prompt)

    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        with st.spinner("Thinking..."):

            st.write_stream(

                chat.chat(
                    session_id=st.session_state.session_id,
                    user_message=prompt,
                )

            )

    st.rerun()