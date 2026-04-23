# Students AI Assistance 🎓🤖

An intelligent, multi-modal AI assistant designed to support students in their academic journey. Leveraging state-of-the-art LLMs, agentic workflows, and voice capabilities to provide a seamless learning experience.

## 🚀 Overview

**Students AI Assistance** is an end-to-end AI platform built for the Generative AI Hackathon. It aims to solve common student challenges like concept clarification, task automation, and interactive learning through a sophisticated agentic architecture.

## ✨ Key Features

- **Multi-Modal Interaction**: Support for both text and voice-based queries.
- **Agentic Workflows**: Powered by `LangGraph` to handle complex reasoning and multi-step tasks.
- **Voice Intelligence**: 
  - Speech-to-Text using **OpenAI Whisper**.
  - Text-to-Speech using **gTTS**.
- **High Performance**: Powered by **Groq** (Llama 3.1) for near-instantaneous responses.
- **Interactive UI**: Clean and intuitive interface built with **Streamlit**.
- **Robust Backend**: Scalable API endpoints using **FastAPI**.

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **LLM Orchestration**: LangChain, LangGraph
- **Inference Engine**: Groq (Llama 3.1)
- **Audio Processing**: OpenAI Whisper, gTTS, SoundDevice, FFmpeg
- **Web Frameworks**: Streamlit (Frontend), FastAPI (Backend)
- **Data Science**: NumPy, Pandas, Scikit-Learn
- **Deep Learning**: Torch, Transformers

## 📂 Project Structure

```text
Students AI Assistance/
├── sources/
│   ├── Agents/          # Agent logic and definitions
│   ├── Model/           # LLM configuration and wrappers
│   ├── workflow/        # LangGraph workflow definitions
│   ├── logger.py        # Logging configuration
│   ├── exception.py     # Custom exception handling
│   └── utils.py         # Utility functions
├── logs/                # Application logs
├── main.py              # Main entry point for CLI/Testing
├── api.py               # FastAPI server implementation
├── pyproject.toml       # Project metadata and dependencies
└── requirements.txt     # Dependency list
```

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.10 or higher
- [Groq API Key](https://console.groq.com/)
- FFmpeg installed on your system (for audio processing)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "Students AI Assistance"
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # OR using uv (recommended)
   uv sync
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Running the Application

- **CLI Mode**:
  ```bash
  python main.py
  ```

- **Web Interface (Coming Soon)**:
  ```bash
  streamlit run app.py
  ```

- **API Server (Coming Soon)**:
  ```bash
  uvicorn api:app --reload
  ```

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
