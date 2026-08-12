import streamlit as st
from backend_sqlite import workflow, checkpointer, get_all_thread_ids
from style import MAIN_STYLE, HEADER_STYLE, BODY_STYLE
from uuid import uuid4

# ****************************** UNTILITES ******************************
def generate_thread_id():
    return str(uuid4())

def new_chat():
    thread_id = generate_thread_id()

    st.session_state['thread_id'] = thread_id

    st.session_state['chat_history'] = []

    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation(thread_id):

    thread_id = str(thread_id)

    st.session_state["thread_id"] = thread_id

    config = {"configurable": {"thread_id": thread_id}}

    current_state = workflow.get_state(config)

    if current_state.values:
        return current_state.values.get("chat_history", [])


def get_thread_id():
    thread_ids = get_all_thread_ids()

    if thread_ids:
        return str(thread_ids[0])

    return generate_thread_id()


def get_all_chat_thread_ids():
    thread_ids = get_all_thread_ids()

    return [str(thread_id) for thread_id in thread_ids]



# ****************************** Session State ******************************

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = get_thread_id()


if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = get_all_chat_thread_ids()


if st.session_state['thread_id'] not in st.session_state['chat_threads']:
    st.session_state['chat_threads'].append(
        st.session_state['thread_id']
    )


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = load_conversation(
        st.session_state['thread_id']
    )


config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

# ****************************** Main UI ******************************

st.set_page_config(
    page_title="My ChatBot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(f"<style>{MAIN_STYLE}</style>", unsafe_allow_html=True)

# ****************************** Sidebar UI ******************************

st.sidebar.text("My ChatBot")

with st.sidebar:

    if st.button("New Chat", use_container_width=True):
        new_chat()
        st.rerun()

    st.header("My Conversations")

    for chat_id in st.session_state['chat_threads']:
        if st.button(
            str(chat_id),
            key=f"chat_{chat_id}",
            use_container_width=True
            ):
            st.session_state['chat_history'] = load_conversation(chat_id)
            st.rerun()



# ****************************** Header ******************************
st.markdown(f"{HEADER_STYLE}", unsafe_allow_html=True)


# ****************************** Body / Welcome ******************************

body_placeholder = st.empty()

if not st.session_state["chat_history"]:
    body_placeholder.markdown(f"{BODY_STYLE}", unsafe_allow_html=True)


# ******************************  Chat History ******************************

for message in st.session_state["chat_history"]:
    with st.chat_message("user"):
        st.write(message["human"])

    with st.chat_message("assistant"):
        st.write(message["assistant"])


# ******************************  Chat Input ******************************

user_input = st.chat_input(
    "Message your AI assistant..."
)


# ******************************  Response ******************************

def stream_response():
    for chunk, metadata in workflow.stream({
        'message': user_input,
        'chat_history': []
    }, config=config, stream_mode='messages'):
        if isinstance(chunk.content, list):
            for block in chunk.content:
                if block.get("type") == "text":
                    yield block['text']
                else:
                    yield block


# ****************************** Handle User Message ******************************

if user_input:

    body_placeholder.empty()

    # Show user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        st.write_stream(stream_response())

    st.session_state['chat_history'] = load_conversation(
        st.session_state['thread_id']
    )

    if st.session_state['thread_id'] not in st.session_state['chat_threads']:

        st.session_state['chat_threads'].append(
            st.session_state['thread_id']
        )

    st.rerun()
