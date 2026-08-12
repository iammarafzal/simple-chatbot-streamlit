import streamlit as st
from backend import workflow
from style import MAIN_STYLE, HEADER_STYLE, BODY_STYLE

st.set_page_config(
    page_title="My ChatBot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(f"<style>{MAIN_STYLE}</style>", unsafe_allow_html=True)


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = "user-1"


config = {
    "configurable": {
        "thread_id": st.session_state["thread_id"]
    }
}


st.markdown(f"{HEADER_STYLE}", unsafe_allow_html=True)


current_state = workflow.get_state(config)

chat_history = []

if current_state.values:
    chat_history = current_state.values.get(
        "chat_history",
        []
    )

if not chat_history:

    st.markdown(f"{BODY_STYLE}", unsafe_allow_html=True)


for message in chat_history:

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

