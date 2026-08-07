from app.database.init_db import DatabaseInitializer
DatabaseInitializer().initialize_database()

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

if "delete_session" not in st.session_state:
    st.session_state.delete_session = None

chat = st.session_state.chat_service

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    if st.button(
        "➕ New Chat",
        use_container_width=False,
        type="primary",
    ):

        st.session_state.session_id = (
            st.session_state.session_manager.create_session()
        )

        st.rerun()

    # st.divider()

    # st.subheader("💬 Conversations")
    st.header("Chats")

    sessions = chat.get_all_sessions()

    if sessions:

        for session in sessions:

            active = session.session_id == st.session_state.session_id

            icon = "🟢" if active else "🟡"

            col1, col2 = st.columns([9, 2])

            with col1:

                if st.button(
                    session.title,
                    key=f"chat_{session.session_id}",
                    icon=icon,
                    use_container_width=False,
                    type="tertiary",
                ):
                    st.session_state.session_id = session.session_id
                    st.rerun()

            with col2:

                with st.popover("⋮"):

                    if st.button(
                        "🗑 Delete Chat",
                        key=f"delete_{session.session_id}",
                        use_container_width=True,
                    ):
                        st.session_state.delete_session = session.session_id
                        st.rerun()

    else:

        st.info("No conversations yet.")

    st.divider()

    st.subheader("⚙️ Model Configuration")

    st.write(f"**Provider:** {settings.llm.provider}")
    st.write(f"**Model:** {settings.llm.model_name}")
    st.write(f"**Streaming:** {'✅ Enabled' if settings.llm.stream else '❌ Disabled'}")

if st.session_state.delete_session:

    session = chat.get_session(st.session_state.delete_session)

    @st.dialog("🗑 Delete Chat")
    def confirm_delete():

        st.write("This will permanently delete the following chat:")

        st.info(f"**{session.title}**")

        st.caption("This action cannot be undone.")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Cancel",
                use_container_width=True,
            ):
                st.session_state.delete_session = None
                st.rerun()

        with col2:

            if st.button(
                "Delete",
                type="primary",
                use_container_width=True,
            ):

                chat.delete_chat(session.session_id)

                st.session_state.delete_session = None

                sessions = chat.get_all_sessions()

                if sessions:
                    st.session_state.session_id = sessions[0].session_id
                else:
                    st.session_state.session_id = (
                        st.session_state.session_manager.create_session()
                    )

                st.rerun()

    confirm_delete()

# -------------------------------------------------------
# Header
# -------------------------------------------------------

with st.container(border=False):
    st.markdown("## 🤖 AI Personal ChatBot")

# -------------------------------------------------------
# Current Chat Title
# -------------------------------------------------------

sessions = chat.get_all_sessions()

current_session = chat.get_session(
    st.session_state.session_id
)

if current_session:

    with st.container(border=True):

        st.markdown(
            f"### 📄 {current_session.title}"
        )

        # st.caption(
        #     f"Last updated : {current_session.updated_at.strftime('%d %b %Y • %I:%M %p')}"
        # )

        st.caption(
            f"Last updated : {current_session.updated_at}"
        )

# -------------------------------------------------------
# Conversation
# -------------------------------------------------------

history = chat.get_message_history(
    st.session_state.session_id
)

with st.container(border=True):

    if not history:

        st.markdown("## 👋 Welcome")

        st.write(
            "Start a conversation with your AI assistant."
        )

    else:

        for message in history:

            avatar = (
                "👨‍💻"
                if message["role"] == "user"
                else "🤖"
            )

            with st.chat_message(message["role"], avatar=avatar):
                if message["role"] == "user":
                    with st.container(border=True):
                        st.markdown(message["content"])
                else:
                    with st.container(border=True):
                        st.markdown(message["content"])

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

        status = st.empty()
        response = st.empty()

        # Initial status
        status.info("🤔 Thinking...")

        full_response = ""
        first_chunk = True

        for chunk in chat.chat(
            session_id=st.session_state.session_id,
            user_message=prompt,
        ):

            # First token received
            if first_chunk:
                # status.info("⚡ Generating response...")
                status.info("✍️ Generating response...")
                first_chunk = False

            full_response += chunk
            response.markdown(full_response + "▌")

        # Final response
        response.markdown(full_response)

        # Remove status
        status.empty()

    st.rerun()