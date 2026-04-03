# 💰 Financial Transaction RAG Chatbot

A production-ready Streamlit application that uses Retrieval-Augmented Generation (RAG) to answer questions about financial transaction data.

## 🌟 Features

- **🔍 Semantic Search**: Find relevant transaction information using vector similarity
- **💬 Interactive Chat**: Natural conversation interface for querying your data
- **📁 File Upload**: Easy data ingestion from text files
- **🤖 Powered by Groq**: Fast LLM inference with Llama 3.3
- **💾 Persistent Storage**: ChromaDB vector database for efficient retrieval
- **⚙️ Configurable**: Adjust model parameters, retrieval settings, and more

## 🏗️ Project Structure

```
financial-rag-chatbot/
├── .env                     # Environment variables (create from .env.example)
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── config.py              # Configuration management
├── data/
│   └── raw/               # Upload your transaction data here
├── chroma_db/             # Vector database (auto-generated)
├── src/                   # Core RAG logic
│   ├── embeddings.py      # Embedding model management
│   ├── vectorstore.py     # ChromaDB operations
│   ├── llm.py            # Groq LLM initialization
│   ├── rag_pipeline.py   # RAG chain construction
│   └── utils.py          # Helper functions
├── app/                   # Streamlit application
│   ├── main.py           # Main app entry point
│   ├── components/       # UI components
│   │   ├── sidebar.py
│   │   ├── chat.py
│   │   └── file_upload.py
│   └── styles/
│       └── custom.css    # Custom styling
└── tests/                # Unit tests
    └── test_rag_pipeline.py
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd financial-rag-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```bash
GROQ_API_KEY=your_actual_api_key_here
```

**Get your Groq API key**: https://console.groq.com

### 5. Add Your Data

Place your transaction data file (`.txt` format) in the `data/raw/` directory, or use the file upload feature in the app.

### 6. Run the Application

```bash
streamlit run app/main.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### First Time Setup

1. **Enter API Key**: If not using `.env`, enter your Groq API key in the sidebar
2. **Upload Data**: Go to "Data Management" tab and upload your transaction file
3. **Process File**: Click "Process File" to build the vector database
4. **Start Chatting**: Go to "Chat" tab and ask questions!

### Sample Questions

- "What are the major expense categories?"
- "Tell me about investment related transactions"
- "What EMI payments are there?"
- "Summarize the travel expenses"
- "What is the average transaction amount?"

### Configuration Options

**Sidebar Settings:**
- **LLM Model**: Choose from Llama 3.3, Llama 3.1, or Mixtral models
- **Temperature**: Control randomness (0 = deterministic, 1 = creative)
- **Top-K Results**: Number of documents to retrieve for context

## 🛠️ Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Structure

**Core Components:**
- `src/embeddings.py`: Manages HuggingFace embeddings (all-MiniLM-L6-v2)
- `src/vectorstore.py`: ChromaDB vector database operations
- `src/llm.py`: Groq LLM initialization and management
- `src/rag_pipeline.py`: RAG chain construction and query execution

**UI Components:**
- `app/components/sidebar.py`: Configuration and settings
- `app/components/chat.py`: Chat interface and message handling
- `app/components/file_upload.py`: File upload and processing

### Adding New Features

1. **New UI Component**: Add to `app/components/`
2. **New Utility**: Add to `src/utils.py`
3. **Configuration**: Add to `config.py`
4. **Tests**: Add to `tests/`

## 📋 Requirements

- Python 3.8+
- Groq API key (free tier available)
- 2GB+ RAM recommended

## 🔧 Troubleshooting

### "No vector database found"
- Upload a data file through the Data Management tab
- Or place a `.txt` file in `data/raw/` and click "Rebuild Vector Database"

### "Invalid API key"
- Ensure your Groq API key starts with `gsk_`
- Check that `.env` file is in the root directory
- Verify the key is correct at https://console.groq.com

### Slow responses
- Try using the `llama-3.1-8b-instant` model for faster inference
- Reduce Top-K results in sidebar settings
- Check your internet connection

## 📦 Dependencies

Core libraries:
- **Streamlit**: Web application framework
- **LangChain**: RAG pipeline orchestration
- **ChromaDB**: Vector database
- **Groq**: Fast LLM inference
- **Sentence Transformers**: Text embeddings

See `requirements.txt` for complete list.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Groq](https://groq.com/)
- Uses [LangChain](https://langchain.com/) for RAG
- Embeddings from [Sentence Transformers](https://www.sbert.net/)

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Happy Chatting! 💬**