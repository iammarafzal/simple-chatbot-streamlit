import streamlit as st
from backend.backend import workflow, memory
from ..style import MAIN_STYLE, HEADER_STYLE, BODY_STYLE
from uuid import uuid4

# ****************************** UNTILITES ******************************
def generate_thread_id():
    thread_id = uuid4()
    return thread_id

def handle_ids(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def new_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    st.session_state['chat_threads'].append(thread_id)
    st.session_state['chat_history'] = []

def load_conversation(thread_id):

    st.session_state["thread_id"] = thread_id

    config = {"configurable": {"thread_id": thread_id}}

    current_state = workflow.get_state(config)

    chat_history = []

    if current_state.values:
        chat_history = current_state.values.get("chat_history", [])

    return chat_history


def get_thread_id():
    thread_ids = list(memory.storage.keys())

    thread_id = ""

    if len(thread_ids) >= 1:
        thread_id = thread_ids[-1]
    else:
        thread_id = generate_thread_id()

    return thread_id

def get_all_thread_ids():
    thread_ids = list(memory.storage.keys())

    if len(thread_ids) >= 1:
        return thread_ids
    else:
        return [st.session_state['thread_id']]

# ****************************** Session ******************************
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = get_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = get_all_thread_ids()

config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = load_conversation(st.session_state['thread_id'])

# ****************************** MAIN UI ******************************
st.set_page_config(
    page_title="My ChatBot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(f"<style>{MAIN_STYLE}</style>", unsafe_allow_html=True)

# ****************************** SIDEBAR UI ******************************
st.sidebar.text("My ChatBot")

with st.sidebar:
    if st.button("New Chat"):
        new_chat()

    st.header("My Conversations")

    for chat_id in st.session_state['chat_threads'][::-1]:
        if st.button(str(chat_id)):
            st.session_state['chat_history'] = load_conversation(chat_id)
            st.rerun()


st.markdown(f"{HEADER_STYLE}", unsafe_allow_html=True)


# ****************************** HANDLE CHAT HISTORY ******************************

if st.session_state["chat_history"] == []:
    st.markdown(f"{BODY_STYLE}", unsafe_allow_html=True)

for message in st.session_state["chat_history"]:
    with st.chat_message("user"):
        st.write(message["human"])

    with st.chat_message("assistant"):
        st.write(message["assistant"])


user_input = st.chat_input(
    "Message your AI assistant..."
)

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

        
if user_input:

    # Show user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        st.write_stream(stream_response())

