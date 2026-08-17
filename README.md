# Simple Chatbot with Streamlit

This repository demonstrates a compact Streamlit chatbot that routes prompts to Google Gemini via LangChain and orchestrates state using LangGraph. It includes two Streamlit frontends (a synchronous UI and a streaming UI), a small backend workflow, and lightweight styling.

**Key ideas**
- Conversation state is managed with LangGraph's `StateGraph` and checkpointed using `MemorySaver`.
- The language model is `ChatGoogleGenerativeAI` (Gemini). Prompts are built with `ChatPromptTemplate`.
- Two frontends: `frontend.py` (synchronous request/response) and `frontend_streaming.py` (streams assistant output chunks).

**Files**
- `backend.py`: defines the `StateGraph`, the `chat` node/function, model initialization, memory saver, and `workflow` object used by the frontends.
- `frontend.py`: Streamlit chat UI that invokes `workflow.invoke(...)` and displays responses after the model returns.
- `frontend_streaming.py`: Streamlit chat UI that consumes chunks from `workflow.stream(...)` and writes assistant output progressively with `st.write_stream()`.
- `style.py`: CSS and small HTML snippets used by both frontends for consistent appearance.
- `requirements.txt`: project dependencies (install via pip).

Requirements
- Python 3.11+ recommended.
- A Google API credential for Gemini access. Depending on the library configuration you can provide an API key or application credentials via environment variables.

Environment
- Create a `.env` file at the project root (the code uses `python-dotenv`) and set one of the expected credentials. Example options:

- API key approach (simple):

	GOOGLE_API_KEY=your_google_api_key

- Service account / application default credentials approach (recommended for production):

	GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

Note: The exact variable name accepted depends on the Google/connector library you use. `ChatGoogleGenerativeAI` typically reads application default credentials or an API key.

Quickstart
1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

3. Add credentials to `.env` (see Environment section).

4a. Run the synchronous frontend

```powershell
streamlit run frontend.py
```

4b. Run the streaming frontend (progressive assistant output)

```powershell
streamlit run frontend_streaming.py
```

Implementation notes (analysis)
- Model initialization: the code constructs `model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')` in `backend.py`. Change the model string if your project should use a different Gemini release or a custom model.
- Prompt construction: `ChatPromptTemplate.from_messages` uses a system message plus a human template that receives `context` and `question`.
- Chat history trimming: before calling the model the backend keeps only the last 2 exchanges (`chat_history = state['chat_history'][-2:]`), which keeps prompts small. Adjust the slice if you want longer context.
- Memory and state: `MemorySaver` is used as the checkpointer for `StateGraph.compile(...)`. That means conversation snapshots persist between workflow runs (depending on how MemorySaver is configured).
- Frontend config: both frontends set `config = { 'configurable': { 'thread_id': st.session_state['thread_id'] } }` and pass that into workflow calls. That `thread_id` drives per-user/per-thread checkpointing.
- Streaming: `frontend_streaming.py` consumes `workflow.stream(..., stream_mode='messages')` and expects chunks whose `.content` may be a list of blocks with `type: 'text'` entries; the code yields block text to `st.write_stream()`.

Troubleshooting & tips
- Authentication errors: verify `.env` values and ensure the Google credential file path is readable. For API key usage, confirm the key has access to the Gemini API in your Google project.
- Model errors / missing model: confirm the model name (e.g., `gemini-3.1-flash-lite`) is available to your Google project and the client library version supports it.
- Large prompts / timeouts: if you see timeouts or truncated responses, reduce the number of history items sent or paginate long documents before including them in `context`.
- Styling not applied: both frontends call `st.markdown(..., unsafe_allow_html=True)` for raw CSS/HTML. If styling doesn't appear, ensure Streamlit version supports the CSS targets used in `style.py`.

Extending
- Increase conversation memory: change the trimming logic in `backend.py` to include more history, or add a retrieval step to inject relevant context from a vector DB.
- Add user IDs: `st.session_state['thread_id']` is currently a simple static value. Integrate a proper user/session identifier if deploying to multiple users.

What's changed in this README
- Expanded file descriptions and clear quickstart commands for both frontends.
- Added explanation of state, memory saver, prompt trimming, and streaming behavior.
- Documented environment/credential options and common troubleshooting steps.

Next steps you might want me to do
- Add example `.env.example` with a minimal set of env vars.
- Validate and pin the `requirements.txt` packages to the minimal working set.
- Add a short demo script or sample conversation recorded in `examples/`.

If you'd like I can also open a PR with these changes, run the app locally, or add an `.env.example` file.
