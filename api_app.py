"""
FastAPI backend for the Financial RAG Chatbot.
Exposes the core src/ logic as REST API endpoints.
"""

import os
import sys
from pathlib import Path
from typing import Optional
import asyncio

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure project root is on PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parent))

import config
from src.vectorstore import VectorStoreManager
from src.llm import LLMManager
from src.rag_pipeline import RAGPipeline

# ---------------------------------------------------------------------------
# App Initialisation
# ---------------------------------------------------------------------------
app = FastAPI(title="Financial RAG Chatbot API", version="1.0.0")

# Allow the Vite dev-server (port 5173) and any localhost origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# In-memory application state (simple single-process server)
# ---------------------------------------------------------------------------
class AppState:
    def __init__(self):
        self.api_key: str = config.GROQ_API_KEY or ""
        self.model_name: str = config.LLM_MODEL
        self.temperature: float = config.TEMPERATURE
        self.top_k: int = config.TOP_K_RESULTS
        self.vectorstore_manager: Optional[VectorStoreManager] = None
        self.rag_pipeline: Optional[RAGPipeline] = None
        self.vectorstore_ready: bool = False

state = AppState()


def _try_load_vectorstore():
    """Attempt to load an existing vectorstore on startup."""
    try:
        vm = VectorStoreManager()
        vs = vm.load_vectorstore()
        if vs is not None:
            state.vectorstore_manager = vm
            state.vectorstore_ready = True
            _rebuild_pipeline()
            print("✅ Vectorstore loaded on startup")
    except Exception as e:
        print(f"⚠️ Could not load vectorstore on startup: {e}")


def _rebuild_pipeline():
    """(Re)build the RAG pipeline from current state."""
    if not state.api_key or not state.vectorstore_ready:
        state.rag_pipeline = None
        return
    retriever = state.vectorstore_manager.get_retriever(k=state.top_k)
    llm = LLMManager.get_llm(
        api_key=state.api_key,
        model=state.model_name,
        temperature=state.temperature,
    )
    state.rag_pipeline = RAGPipeline(llm, retriever)


@app.on_event("startup")
async def on_startup():
    # Run the heavy load operation in a background thread so the server port binds immediately
    asyncio.create_task(run_in_threadpool(_try_load_vectorstore))


# ---------------------------------------------------------------------------
# Pydantic request / response models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    chart_data: Optional[list] = None

class SettingsPayload(BaseModel):
    api_key: Optional[str] = None
    model_name: Optional[str] = None
    temperature: Optional[float] = None
    top_k: Optional[int] = None

class StatusResponse(BaseModel):
    vectorstore_ready: bool
    api_key_set: bool
    model_name: str
    temperature: float
    top_k: int


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Return current application status."""
    return StatusResponse(
        vectorstore_ready=state.vectorstore_ready,
        api_key_set=bool(state.api_key),
        model_name=state.model_name,
        temperature=state.temperature,
        top_k=state.top_k,
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Send a query to the RAG pipeline."""
    if not state.api_key:
        raise HTTPException(status_code=400, detail="API key not configured. Go to Settings.")
    if not state.vectorstore_ready:
        raise HTTPException(status_code=400, detail="No vector database. Upload a file first.")
    if state.rag_pipeline is None:
        _rebuild_pipeline()
    if state.rag_pipeline is None:
        raise HTTPException(status_code=500, detail="Failed to initialise RAG pipeline.")
    try:
        response_data = state.rag_pipeline.query(req.message)
        return ChatResponse(
            answer=response_data.get("answer", str(response_data)),
            chart_data=response_data.get("chart_data")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a .txt file and rebuild the vector database."""
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported.")
    # Save file
    file_path = config.DATA_DIR / file.filename
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Rebuild vectorstore
    try:
        vm = VectorStoreManager()
        vm.rebuild_vectorstore()
        state.vectorstore_manager = vm
        state.vectorstore_ready = True
        _rebuild_pipeline()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build vector DB: {e}")

    return {"message": f"File '{file.filename}' uploaded and indexed successfully."}


@app.get("/api/files")
async def list_files():
    """List uploaded data files."""
    if not config.DATA_DIR.exists():
        return {"files": []}
    files = []
    for f in config.DATA_DIR.glob("*.txt"):
        files.append({"name": f.name, "size": f.stat().st_size})
    return {"files": files}


@app.delete("/api/files/{filename}")
async def delete_file(filename: str):
    """Delete a data file."""
    file_path = config.DATA_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    try:
        file_path.unlink()
        return {"message": f"File '{filename}' deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/settings")
async def update_settings(payload: SettingsPayload):
    """Update application settings (API key, model, temperature, top-k)."""
    changed = False
    if payload.api_key is not None:
        state.api_key = payload.api_key
        changed = True
    if payload.model_name is not None:
        state.model_name = payload.model_name
        changed = True
    if payload.temperature is not None:
        state.temperature = payload.temperature
        changed = True
    if payload.top_k is not None:
        state.top_k = payload.top_k
        changed = True

    if changed and state.vectorstore_ready:
        _rebuild_pipeline()

    return {"message": "Settings updated.", "pipeline_ready": state.rag_pipeline is not None}
