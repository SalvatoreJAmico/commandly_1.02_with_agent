# modules/gpt_integration.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASIC_SYSTEM = "You are Commandly. Be concise, helpful, and friendly."

def chat_completion(messages, model="gpt-4o-mini"):
    """Basic chat completion function"""
    try:
        response = client.chat.completions.create(
            model=model, 
            messages=messages, 
            temperature=0.7, 
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def ask_gpt(messages) -> str:
    return chat_completion(messages)

def decide_mode(user_text: str) -> str:
    """Decide whether to use agent mode or chat mode"""
    t = user_text.lower()
    
    # Agent mode triggers - commands that require action
    agent_triggers = [
        "open", "launch", "start", "run", "execute", "install", "create", "make", 
        "build", "add", "write", "modify", "change", "fix", "update", "improve",
        "delete", "remove", "search web", "browse", "download", "upload", "save",
        "file", "folder", "program", "application", "notepad", "calculator", 
        "explorer", "chrome", "firefox", "code", "visual studio", "cmd", "powershell",
        "restart", "shutdown", "reboot", "kill process", "task manager",
        "appearance", "color", "design", "interface", "gui", "animation"
    ]
    
    # Check if any agent triggers are present
    if any(trigger in t for trigger in agent_triggers):
        print(f"🔧 Agent mode triggered by: {[trigger for trigger in agent_triggers if trigger in t]}")
        return "agent"
    
    # Default to chat mode for general conversation
    print("💬 Chat mode - general conversation")
    return "chat"

def chat_completion_json(messages, model="gpt-4o-mini"):
    """Return raw text from the model; intended to be JSON-only according to system prompt."""
    try:
        response = client.chat.completions.create(
            model=model, 
            messages=messages, 
            temperature=0.2, 
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f'{{ "error": "{str(e)}" }}'