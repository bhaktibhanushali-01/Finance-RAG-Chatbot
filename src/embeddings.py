"""
Embeddings module for initializing and managing HuggingFace embeddings.
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import Optional
import config


class EmbeddingsManager:
    """Manages the initialization and caching of embedding models."""
    
    _instance: Optional[HuggingFaceEmbeddings] = None
    
    @classmethod
    def get_embeddings(cls, model_name: str = config.EMBEDDING_MODEL) -> HuggingFaceEmbeddings:
        """
        Get or create embeddings model instance (singleton pattern).
        
        Args:
            model_name: Name of the HuggingFace model to use for embeddings
            
        Returns:
            HuggingFaceEmbeddings instance
        """
        if cls._instance is None:
            print(f"🔄 Loading embeddings model: {model_name}")
            cls._instance = HuggingFaceEmbeddings(model_name=model_name)
            print("✅ Embeddings model loaded successfully")
        
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset the embeddings instance (useful for testing)."""
        cls._instance = None