"""
Configuration management for the Financial RAG Chatbot.
Loads environment variables and defines application constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"
STYLES_DIR = BASE_DIR / "app" / "styles"

# Create directories if they don't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Model configurations
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
LLM_MODEL = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))

# Text splitting configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

# Retrieval configuration
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))

# Prompt template
PROMPT_TEMPLATE = """You are a financial assistant analyzing transaction data.
Use ONLY the context below to answer the question. Be concise and accurate.
If you don't know, say "I don't have enough information."

If the question asks for a breakdown, summary of categories, or any quantitative mapping that can be visualized as a pie chart, generate that chart data as part of your answer.
If no graph is applicable, return null for chart_data.

You MUST respond strictly in valid JSON format matching the following structure:
{{
  "answer": "Your detailed text answer here...",
  "chart_data": [
    {{"name": "Category 1", "value": 100}},
    {{"name": "Category 2", "value": 250}}
  ]
}}
For 'chart_data', use null if not applicable.

Context: {context}

Question: {question}"""

# Streamlit page configuration
PAGE_TITLE = "💰 Financial RAG Chatbot"
PAGE_ICON = "💰"
LAYOUT = "wide"