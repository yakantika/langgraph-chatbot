# LangGraph Chatbot

A sophisticated, multi-threaded chatbot built with LangGraph, Streamlit, and OpenAI's GPT models. This project demonstrates advanced conversation management with persistent storage and thread-based conversations.

## 🚀 Features

- **Multi-threaded Conversations**: Create and switch between different conversation threads
- **Persistent Storage**: All conversations are saved in an SQLite database
- **Modern UI**: Clean, responsive interface built with Streamlit
- **Powered by OpenAI**: Utilizes GPT models for natural language understanding
- **Efficient State Management**: Built with LangGraph for robust conversation flows

## 🛠️ Tech Stack

- **Frameworks**: 
  - LangGraph for conversation state management
  - Streamlit for the web interface
- **AI**: OpenAI GPT models
- **Database**: SQLite for conversation persistence
- **Deployment**: Ready for containerization and cloud deployment

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/langgraph-chatbot.git
   cd langgraph-chatbot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

### Running the Application

```bash
streamlit run src/app.py
```

Then open your browser to `http://localhost:8501`

## 🏗️ Project Structure

```
langgraph-chatbot/
├── src/
│   ├── app.py            # Streamlit frontend
│   └── backend.py        # LangGraph backend and conversation logic
├── tests/                # Test files
├── .env.example          # Example environment variables
├── .gitignore
├── requirements.txt      # Python dependencies
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


##  Acknowledgments

- Built with [LangGraph](https://langchain-ai.github.io/langgraph/)
- UI powered by [Streamlit](https://streamlit.io/)
- AI capabilities by [OpenAI](https://openai.com/)
