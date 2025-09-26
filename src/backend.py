"""
LangGraph Chatbot Backend

This module implements a persistent, thread-aware chatbot using LangGraph and SQLite.
It supports multi-threaded conversations with persistent storage.
"""

from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3
import os

# Load environment variables
load_dotenv()

# Initialize the language model
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    max_tokens=500
)

class ChatState(TypedDict):
    """State definition for the chat application."""
    messages: Annotated[List[BaseMessage], add_messages]

def chat_node(state: ChatState) -> dict:
    """Process chat messages using the language model.
    
    Args:
        state: Current chat state containing message history
        
    Returns:
        dict: Updated state with the model's response
    """
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# Initialize database connection and checkpointer
DATABASE_PATH = os.getenv('DATABASE_PATH', 'chatbot.db')
db_conn = sqlite3.connect(database=DATABASE_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn=db_conn)

# Build the conversation graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile the graph with persistence
chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads() -> List[str]:
    """Retrieve all conversation thread IDs from the database.
    
    Returns:
        List[str]: List of thread IDs
    """
    all_threads = set()
    try:
        for checkpoint in checkpointer.list(None):
            all_threads.add(checkpoint.config['configurable']['thread_id'])
    except Exception as e:
        print(f"Error retrieving threads: {e}")
    return list(all_threads)

def get_conversation_history(thread_id: str) -> List[BaseMessage]:
    """Retrieve conversation history for a specific thread.
    
    Args:
        thread_id: ID of the conversation thread
        
    Returns:
        List[BaseMessage]: List of messages in the conversation
    """
    try:
        state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
        return state.values.get('messages', [])
    except Exception as e:
        print(f"Error loading conversation: {e}")
        return []

# Add proper cleanup on application exit
import atexit

def cleanup():
    """Clean up database connections on application exit."""
    if 'db_conn' in globals():
        db_conn.close()

atexit.register(cleanup)
