"""
LLM module for initializing and managing Groq language models.
"""

from langchain_groq import ChatGroq
from typing import Optional
import config


class LLMManager:
    """Manages the initialization of Groq LLM."""
    
    @staticmethod
    def get_llm(
        api_key: str,
        model: str = config.LLM_MODEL,
        temperature: float = config.TEMPERATURE
    ) -> ChatGroq:
        """
        Initialize and return Groq LLM instance.
        
        Args:
            api_key: Groq API key
            model: Model name to use
            temperature: Temperature for response generation
            
        Returns:
            ChatGroq instance
            
        Raises:
            ValueError: If API key is empty
        """
        if not api_key:
            raise ValueError("Groq API key is required")
        
        print(f"🤖 Initializing LLM: {model} (temperature={temperature})")
        
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model,
            temperature=temperature
        )
        
        print("✅ LLM initialized successfully")
        return llm