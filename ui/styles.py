GLASS_CSS = """
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff 0%, #f5f3ff 40%, #eef9ff 100%);
}

section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: blur(18px);
    border-right: 1px solid rgba(255, 255, 255, 0.4);
}

.glass-panel {
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.08);
    margin-bottom: 16px;
}

.glass-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    background: rgba(99, 102, 241, 0.12);
    color: #4338ca;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 8px;
}

.stButton > button {
    border-radius: 14px;
    border: 1px solid rgba(99, 102, 241, 0.25);
    background: rgba(99, 102, 241, 0.1);
    color: #3730a3;
    font-weight: 600;
    backdrop-filter: blur(10px);
}

.stButton > button:hover {
    background: rgba(99, 102, 241, 0.2);
    border-color: rgba(99, 102, 241, 0.4);
}

.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
    border-radius: 14px !important;
    background: rgba(255, 255, 255, 0.7) !important;
}

h1, h2, h3 {
    color: #1e1b4b;
    font-weight: 700;
}

.stChatMessage {
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(14px);
}
</style>
"""
