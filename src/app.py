"""
LangGraph Chatbot - Streamlit Frontend

A multi-threaded chat interface with persistent conversation history.
"""

import streamlit as st
from backend import chatbot, retrieve_all_threads, get_conversation_history
from langchain_core.messages import HumanMessage
import uuid
from typing import List, Dict, Any
import time

# Page configuration
st.set_page_config(
    page_title="LangGraph Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .thread-button {
        margin: 5px 0;
        width: 100%;
        text-align: left;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    </style>
""", unsafe_allow_html=True)

def generate_thread_id() -> str:
    """Generate a new unique thread ID."""
    return str(uuid.uuid4())

def initialize_session_state():
    """Initialize session state variables."""
    if 'message_history' not in st.session_state:
        st.session_state.message_history = []
    
    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = generate_thread_id()
    
    if 'chat_threads' not in st.session_state:
        st.session_state.chat_threads = retrieve_all_threads()
        if st.session_state.thread_id not in st.session_state.chat_threads:
            st.session_state.chat_threads.append(st.session_state.thread_id)

def reset_chat():
    """Reset the current chat and create a new thread."""
    thread_id = generate_thread_id()
    st.session_state.thread_id = thread_id
    if thread_id not in st.session_state.chat_threads:
        st.session_state.chat_threads.append(thread_id)
    st.session_state.message_history = []
    st.rerun()

def load_conversation(thread_id: str):
    """Load conversation history for a specific thread."""
    st.session_state.thread_id = thread_id
    messages = get_conversation_history(thread_id)
    
    st.session_state.message_history = []
    for msg in messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        st.session_state.message_history.append({"role": role, "content": msg.content})
    
    # Rerun to update the UI
    st.rerun()

def render_sidebar():
    """Render the sidebar with thread management."""
    with st.sidebar:
        st.title("💬 Chat Threads")
        
        if st.button("➕ New Chat", use_container_width=True):
            reset_chat()
        
        st.markdown("---")
        st.subheader("Your Conversations")
        
        # Display conversation threads with timestamps if available
        for thread_id in reversed(st.session_state.chat_threads):
            # Truncate the thread ID for display
            display_id = f"{thread_id[:8]}..."
            if st.button(
                f"💬 {display_id}",
                key=f"thread_{thread_id}",
                on_click=load_conversation,
                args=(thread_id,),
                use_container_width=True
            ):
                pass

def render_chat_messages():
    """Render the chat message history."""
    for message in st.session_state.message_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    """Handle user input and generate responses."""
    if user_input := st.chat_input("Type your message..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Add to message history
        st.session_state.message_history.append({"role": "user", "content": user_input})
        
        # Prepare the configuration for the chatbot
        config = {
            "configurable": {"thread_id": st.session_state.thread_id},
            "metadata": {"thread_id": st.session_state.thread_id},
            "run_name": "chat_turn",
        }
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            for chunk in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=config,
                stream_mode="messages"
            ):
                if hasattr(chunk[0], 'content'):
                    full_response += chunk[0].content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Update message history
            st.session_state.message_history.append({
                "role": "assistant",
                "content": full_response
            })

def main():
    """Main application function."""
    st.title("🤖 LangGraph Chatbot")
    
    # Initialize session state
    initialize_session_state()
    
    # Render the UI
    render_sidebar()
    
    # Display chat messages
    render_chat_messages()
    
    # Handle user input
    handle_user_input()

if __name__ == "__main__":
    main()
