# 💰 Financial Transaction AI Analyst

![Architecture](https://img.shields.io/badge/Architecture-FastAPI%20%2B%20React-blue?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg?style=for-the-badge&logo=python)
![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-purple.svg?style=for-the-badge)
![Groq](https://img.shields.io/badge/LLM-Groq-orange.svg?style=for-the-badge)
![Recharts](https://img.shields.io/badge/Charts-Recharts-cyan.svg?style=for-the-badge)

An enterprise-grade, production-ready AI application that uses Retrieval-Augmented Generation (RAG) to dynamically answer questions, graph trends, and deeply analyze your raw financial transaction data.

---

## 🌟 Highlights & Features

- **Dynamic Data Visualization:** Automatically generates context-aware, completely animated **Pie Charts** whenever you ask about expense categories, quantitative breakdowns, or spending summaries. Powered by structured JSON-mode LLM responses and `recharts`.
- **Premium User Interface:** A gorgeous, luxurious "Obsidian & Gold" color palette built in native React. Includes custom micro-animations, glassmorphism layouts, and an ambient 3D Aurora Mesh gradient background.
- **Robust AI Backend Engine:** Fully decoupled FastAPI backend delivering lightning-fast vector retrieval and inference routing.
- **Local Dense Retrieval:** Seamless document stream ingestion mapped locally to a high-speed `ChromaDB` vector database utilizing HuggingFace `all-MiniLM-L6-v2` embeddings.
- **Hardware-Enforced Logic:** Configured against the Groq API (Llama 3 generation) using native JSON Object Mode enforcement, drastically eliminating delimiter/formatting errors when passing graph data to the frontend.

## 🏗️ System Architecture

The project operates through a modernized, decoupled architecture cleanly separating the AI/Vector layer from the DOM/UI layer:

```text
financial-rag-chatbot/
├── .env                     # Global environment variables
├── run.bat                  # One-click startup script for Windows developers
├── api_app.py               # FastAPI backend entrypoint (Routers)
├── src/                     # Core Backend Logic Context
│   ├── embeddings.py        # Sentence Embedder Generator
│   ├── vectorstore.py       # Local ChromaDB Layer
│   ├── llm.py               # Groq LLM Connection with JSON Enforcement
│   └── rag_pipeline.py      # LangChain Retriever + QA Chain
├── frontend/                # React Vite Application Layer
│   ├── src/
│   │   ├── api.js           # REST API fetch interface
│   │   ├── App.jsx          # Root Layout & Main Grid
│   │   ├── index.css        # Premium Design System Variables
│   │   └── components/      # UI Web Components (ChatPanel, ChartWrapper)
│   └── package.json         # UI Dependencies
└── data/                    # Storage for localized transaction docs
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.8+**
- **Node.js 18+** & **npm**
- **Groq API Key**: Get one for free at the [Groq Console](https://console.groq.com).

### 2. Configure Backend Environment
Open your terminal and create your Python virtual environment:

```bash
# Clone the repository
git clone <your-repo-url>
cd financial-rag-chatbot

# Create and activate virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# Install Core Backend Dependencies
pip install -r requirements.txt
```

Prepare the configuration block:
```bash
# Create an `.env` file in the root
type NUL > .env
```
Open the `.env` file and define your active LLM API credentials:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

### 4. Running the Complete Application Stack
For absolute convenience on Windows, a dual-thread automation batch script is provided. Double-click **`run.bat`** or run it via the terminal:
```bash
.\run.bat
```

This successfully spawns:
- **The FastAPI Services Server** simultaneously bound to `http://localhost:8000`
- **The React Vite Build Server** instantly bound to `http://localhost:5173`

*(Your frontend will automatically begin accepting events at `http://localhost:5173`)*

---

## 📖 Usage Walkthrough

1. **Upload Data:** Expand the left sidebar document panel. Drag and drop any `.txt` financial transaction logs into the target zone. The backend immediately computes your embeddings and mounts the data into `ChromaDB`.
2. **Text Analysis:** Ask conversational inquiries in the primary chat, such as:
   - *"Were there any strange investment transactions last week?"*
   - *"Did I purchase any recurring subscriptions?"*
3. **Trigger Visualizations:** Prompt the assistant for structured numerical breakdowns. The intelligent backend will natively compile mathematical parameters securely into JSON, prompting the UI to slide open the Visualization Panel:
   - *"What are the major expense categories in my data?"*
   - *"Summarize the travel expenses versus food."*

---

## 🔒 Contributing & Pushing to GitHub
Your local project tree contains an updated `.gitignore` meticulously configured to filter `chroma_db/`, `.env`, and uncompiled `.pyc` caches. You are completely safe to initialize this repository and `git push` without securely leaking keys or vector embeddings.

## 📄 License
This application is distributed under the MIT License. See the LICENSE file for details.