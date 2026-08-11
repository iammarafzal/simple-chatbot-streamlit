MAIN_STYLE = """

    /* Main container */
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }

    /* Header */
    .chat-header {
        text-align: center;
        padding: 1rem 0 2rem 0;
    }

    .chat-header h1 {
        font-size: 2.2rem;
        margin-bottom: 0.3rem;
    }

    .chat-header p {
        color: #888;
        font-size: 1rem;
        margin-top: 0;
    }

    /* Welcome card */
    .welcome-card {
        text-align: center;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 16px;
        background: rgba(128, 128, 128, 0.05);
    }

    .welcome-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .welcome-card h3 {
        margin-bottom: 0.5rem;
    }

    .welcome-card p {
        color: #888;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.2);
    }

    /* Chat input */
    div[data-testid="stChatInput"] {
        padding-bottom: 1rem;
    }

"""

HEADER_STYLE = """
<div class="chat-header">
    <h1>🤖 My ChatBot</h1>
    <p>Your AI assistant powered by Gemini</p>
</div>
"""

BODY_STYLE = """
    <div class="welcome-card">
        <div class="welcome-icon">👋</div>
        <h3>Welcome!</h3>
        <p>
            I'm your AI assistant. Ask me anything to get started.
        </p>
    </div>
"""