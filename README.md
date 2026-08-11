# Simple Chatbot with Streamlit

A lightweight Streamlit chatbot app that uses Google Gemini through LangChain and LangGraph.

## Overview

This project demonstrates a simple conversational AI interface with:

- `Streamlit` for the web UI
- `langgraph` for workflow state management
- `langchain-google-genai` and `ChatGoogleGenerativeAI` for Google Gemini model access
- `dotenv` for environment-based credentials

The frontend renders a chat interface, while the backend defines a `StateGraph` workflow with a single chat node.

## Features

- Streamlit chat UI with user and assistant message bubbles
- Gemini model prompt pipeline using system + human role messages
- Stateful conversation memory via LangGraph checkpointing
- Custom page styling from `style.py`

## Project files

- `frontend.py` - Streamlit app entry point
- `backend.py` - Chat workflow, model setup, and state graph definition
- `style.py` - UI styles and welcome card HTML
- `requirements.txt` - pinned Python dependencies
- `README.md` - project documentation

## Prerequisites

- Python 3.11+ recommended
- Google Cloud credentials for Gemini access
- `pip` installed

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Google credentials.

Example using an API key:

```env
GOOGLE_API_KEY=your_google_api_key
```

4. Start the app:

```powershell
streamlit run frontend.py
```

5. Open the local URL printed by Streamlit in your browser.

## Usage

- Type a message in the chat input at the bottom of the page.
- The assistant sends the prompt to Gemini with recent conversation context.
- Responses appear as assistant messages in the chat history.

## Notes

- `backend.py` uses `ChatPromptTemplate.from_messages` to format a system message and a human message.
- The chat history is trimmed to the last 2 exchanges before sending context to the model.
- The UI currently uses a single `thread_id` stored in `st.session_state`.

## Troubleshooting

- If the app cannot authenticate, verify your `.env` values and Google credentials.
- If Gemini model calls fail, ensure the model name `gemini-3.1-flash-lite` is available in your Google project.
- If Streamlit styling does not render, confirm `unsafe_allow_html=True` is enabled for HTML markdown.

## Dependency management

Use `requirements.txt` to reinstall exact versions.

```powershell
python -m pip install -r requirements.txt
```

## License

This repository has no license specified.
