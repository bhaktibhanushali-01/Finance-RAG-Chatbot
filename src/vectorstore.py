"""
Vector store module for managing ChromaDB operations.
"""

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from typing import Optional, List
import shutil
import config
from src.embeddings import EmbeddingsManager


class VectorStoreManager:
    """Manages ChromaDB vector store operations."""
    
    def __init__(self):
        self.embeddings = EmbeddingsManager.get_embeddings()
        self.vectorstore: Optional[Chroma] = None
        self.retriever = None
    
    def load_documents(self, data_dir: Path = config.DATA_DIR) -> List:
        """
        Load documents from directory.
        
        Args:
            data_dir: Path to directory containing text files
            
        Returns:
            List of loaded documents
        """
        print(f"📂 Loading documents from: {data_dir}")
        
        loader = DirectoryLoader(
            str(data_dir),
            glob="*.txt",
            loader_cls=TextLoader
        )
        documents = loader.load()
        
        print(f"✅ Loaded {len(documents)} document(s)")
        return documents
    
    def split_documents(self, documents: List) -> List:
        """
        Split documents into chunks.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of document chunks
        """
        print(f"✂️ Splitting documents (chunk_size={config.CHUNK_SIZE}, overlap={config.CHUNK_OVERLAP})")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        chunks = text_splitter.split_documents(documents)
        
        print(f"✅ Created {len(chunks)} chunks")
        return chunks
    
    def create_vectorstore(
        self,
        chunks: List,
        persist_directory: Path = config.CHROMA_DB_DIR
    ) -> Chroma:
        """
        Create and persist vector store.
        
        Args:
            chunks: List of document chunks
            persist_directory: Directory to persist the vector store
            
        Returns:
            Chroma vector store instance
        """
        print(f"🔨 Creating vector store at: {persist_directory}")
        
        self.vectorstore = Chroma.from_documents(
            chunks,
            self.embeddings,
            persist_directory=str(persist_directory)
        )
        
        print("✅ Vector store created successfully")
        return self.vectorstore
    
    def load_vectorstore(
        self,
        persist_directory: Path = config.CHROMA_DB_DIR
    ) -> Optional[Chroma]:
        """
        Load existing vector store.
        
        Args:
            persist_directory: Directory where vector store is persisted
            
        Returns:
            Chroma vector store instance or None if doesn't exist
        """
        if not persist_directory.exists():
            print(f"⚠️ Vector store not found at: {persist_directory}")
            return None
        
        print(f"📥 Loading vector store from: {persist_directory}")
        
        self.vectorstore = Chroma(
            persist_directory=str(persist_directory),
            embedding_function=self.embeddings
        )
        
        print("✅ Vector store loaded successfully")
        return self.vectorstore
    
    def get_retriever(self, k: int = config.TOP_K_RESULTS):
        """
        Get retriever from vector store.
        
        Args:
            k: Number of documents to retrieve
            
        Returns:
            Retriever instance
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Call load_vectorstore() or create_vectorstore() first.")
        
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
        
        return self.retriever
    
    def rebuild_vectorstore(self, data_dir: Path = config.DATA_DIR) -> Chroma:
        """
        Rebuild vector store from scratch.
        
        Args:
            data_dir: Path to directory containing text files
            
        Returns:
            New Chroma vector store instance
        """
        print("🔄 Rebuilding vector store...")
        
        # Delete existing vector store
        if config.CHROMA_DB_DIR.exists():
            shutil.rmtree(config.CHROMA_DB_DIR)
            print("🗑️ Deleted old vector store")
        
        # Load and process documents
        documents = self.load_documents(data_dir)
        chunks = self.split_documents(documents)
        
        # Create new vector store
        vectorstore = self.create_vectorstore(chunks)
        
        print("✅ Vector store rebuilt successfully")
        return vectorstore