import streamlit as st
import requests
from datetime import datetime
import json

from src.config import settings

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title=settings.app.page_title,
    page_icon="🤖",
    layout="wide",
)

# API Configs
chat_url= settings.api_settings.chat_url
session_url = settings.api_settings.session_url
headers = settings.api_settings.headers

# -------------------------------------------------------
# Session State
# -------------------------------------------------------

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "delete_session" not in st.session_state:
    st.session_state.delete_session = None

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    with st.container(border=False):
        st.markdown("## 🤖 AI Personal ChatBot")
        
    if st.button(
        "➕ New Chat",
        use_container_width=False,
        type="primary",
    ):

        st.session_state.session_id = None

        st.rerun()

    st.header("Chats")

    response = requests.get(session_url, headers=headers)
    sessions = response.json()

    if sessions:

        for session in sessions:

            active = session["session_id"] == st.session_state.session_id

            icon = "🟢" if active else "🟡"

            col1, col2 = st.columns([9, 2])

            with col1:

                if st.button(
                    session["title"],
                    key=f"chat_{session['session_id']}",
                    icon=icon,
                    use_container_width=False,
                    type="tertiary",
                ):
                    st.session_state.session_id = session["session_id"]
                    st.rerun()

            with col2:

                with st.popover("⋮"):

                    if st.button(
                        "🗑 Delete Chat",
                        key=f"delete_{session['session_id']}",
                        use_container_width=True,
                    ):
                        st.session_state.delete_session = session["session_id"]
                        st.rerun()

    else:

        st.info("No conversations yet.")

    st.divider()

    st.subheader("⚙️ Model Configuration")

    st.write(f"**Provider:** {settings.llm.provider}")
    st.write(f"**Model:** {settings.llm.model_name}")
    st.write(f"**Streaming:** {'✅ Enabled' if settings.llm.stream else '❌ Disabled'}")

if st.session_state.delete_session:
    delete_session_id = st.session_state.delete_session
    get_session_url = f"{session_url}/{delete_session_id}"
    response = requests.get(get_session_url, headers=headers)
    delete_session = response.json()

    @st.dialog("🗑 Delete Chat")
    def confirm_delete():

        st.write("This will permanently delete the following chat:")

        st.info(f"**{delete_session['title']}**")

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

                # delete_session_url = f"{session_url}/{session['session_id']}"
                delete_session_url = f"{session_url}/{delete_session_id}"
                requests.delete(delete_session_url, headers=headers)

                st.session_state.delete_session = None

                response = requests.get(session_url, headers=headers)
                sessions = response.json()

                if sessions:
                    st.session_state.session_id = sessions[0]["session_id"]
                else:
                    # No persisted conversations remain
                    st.session_state.session_id = None

                st.rerun()

    confirm_delete()

# -------------------------------------------------------
# Header
# -------------------------------------------------------

# with st.container(border=False):
#     st.markdown("## 🤖 AI Personal ChatBot")

# -------------------------------------------------------
# Current Chat Title
# -------------------------------------------------------

current_session = None

if st.session_state.session_id:
    get_session_url = f"{session_url}/{st.session_state.session_id}"
    response = requests.get(get_session_url, headers=headers)
    current_session = response.json()

if current_session:

    with st.container(border=False):

        st.markdown(
            f"#### 📄 {current_session['title']}"
        )

        updated_at = datetime.fromisoformat(current_session["updated_at"])

        st.caption(
            f"Last updated: {updated_at.strftime('%d %b %Y • %I:%M %p')}"
        )
else:

    with st.container(border=True):
        st.markdown("### 📄 New Chat")

# -------------------------------------------------------
# Conversation
# -------------------------------------------------------

get_history_url = f"{session_url}/{st.session_state.session_id}/messages"
response = requests.get(get_history_url, headers=headers)
history = response.json()

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
        response_container = st.empty()

        # Initial status
        status.info("🤔 Thinking...")

        first_chunk = True

        response = requests.post(
            chat_url,
            headers=headers,
            json={
                "session_id": st.session_state.session_id,
                "query": prompt
                },
            stream=True
            )

        full_response = ""

        for line in response.iter_lines(
            decode_unicode=True,
            chunk_size=None
            ):

            if not line:
                continue

            llm_response = json.loads(line)

            # Update active session
            st.session_state.session_id = llm_response["session_id"]

            # First token received
            if first_chunk:
                # status.info("⚡ Generating response...")
                status.info("✍️ Generating response...")
                first_chunk = False

            full_response += llm_response["llm_response"]
            response_container.markdown(full_response + "▌")

        # Final response
        response_container.markdown(full_response)

        # Remove status
        status.empty()

    st.rerun()