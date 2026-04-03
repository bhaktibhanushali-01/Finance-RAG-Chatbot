# 💰 Financial Transaction RAG Chatbot

![Architecture](https://img.shields.io/badge/Architecture-FastAPI%20%2B%20React-blue?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg?style=for-the-badge&logo=python)
![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-purple.svg?style=for-the-badge)
![Groq](https://img.shields.io/badge/LLM-Groq-orange.svg?style=for-the-badge)

An enterprise-grade, production-ready AI application that uses Retrieval-Augmented Generation (RAG) to answer questions and analyze your financial transaction data.

## 🌟 Highlights

- **Aesthetic UI:** Premium dark-themed React frontend built with Vite, featuring glassmorphism and micro-animations.
- **Robust API:** Fully decoupled FastAPI backend delivering lightning-fast model inference endpoints.
- **Semantic Search:** Ingests document streams and retrieves contextually relevant financial anomalies and historical spending via ChromaDB.
- **LLM Agnostic:** Out-of-the-box integration with Groq API (Llama 3.3, Llama 3.1, Mixtral) for blazingly fast token generation.

## 🏗️ System Architecture

The project has evolved into a modern decoupled architecture:

```
financial-rag-chatbot/
├── .env                     # Global environment variables
├── run.bat                  # One-click startup script for Windows
├── api_app.py               # FastAPI backend entrypoint
├── src/                     # Core Backend Framework Layer
│   ├── embeddings.py        # HuggingFace MiniLM Embeddings
│   ├── vectorstore.py       # ChromaDB interactions Layer
│   ├── llm.py               # Groq LLM initialization
│   ├── rag_pipeline.py      # Core RAG logic and LangChain pipelines
│   └── utils.py             # Server-side utils
├── frontend/                # React Vite Application Layer
│   ├── src/
│   │   ├── api.js           # REST API fetch calls
│   │   ├── App.jsx          # Root Layout
│   │   ├── index.css        # Vanilla CSS Design System
│   │   └── components/      # UI Web Components (Sidebar, ChatPanel)
│   └── package.json
└── data/                    # Local storage for transaction docs and Chroma index
```

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.8+**
- **Node.js 18+** & **npm**
- **Groq API Key**: Get one for free at [Groq Console](https://console.groq.com)

### 2. Setup the Environment

Open your terminal and create your Python virtual environment:

```bash
# Clone the repository
git clone <your-repo-url>
cd financial-rag-chatbot

# Create and activate virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# Install Backend Dependencies
pip install -r requirements.txt
```

Set up your API Key in the root of your project:
```bash
cp .env.example .env
# Edit .env and paste in your GROQ_API_KEY
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Running the Application Stack

We have provided a one-click startup script for Windows. Simply double-click **`run.bat`**, or run it from the terminal:

```bash
.\run.bat
```

This will concurrently boot:
- **FastAPI Backend Services** on `http://localhost:8000`
- **React Frontend Application** on `http://localhost:5173`

*(The frontend will be readily available in your browser at `http://localhost:5173`)*

---

## 📖 Usage Guide

1. **Configure Model**: Once the UI loads, open the Settings tab on the left sidebar to confirm your API Key and select your preferred LLM model.
2. **Ingest Data**: Switch to the Documents tab. Drag and drop your `.txt` financial transaction logs into the drop zone. The system will automatically compute embeddings and populate the local ChromaDB vector store.
3. **Query Engine**: Go to the central chat area and ask context-heavy questions like:
   - *"What were my major expense categories last month?"*
   - *"Summarize any anomalies in my investment transactions."*

Your frontend operates fully asynchronously with the backend AI engine, maintaining history and session-based contexts seamlessly.

---

## 💻 Tech Stack
- **API Engine**: FastAPI, Uvicorn
- **AI / LLM Framework**: LangChain, Groq SDK
- **Embeddings**: Sentence-Transformers `all-MiniLM-L6-v2`
- **Vector Database**: ChromaDB
- **Web UI Engine**: React 19, Vite, Vanilla CSS

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.