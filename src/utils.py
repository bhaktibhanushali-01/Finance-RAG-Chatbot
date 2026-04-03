"""
Utility functions for the Financial RAG Chatbot.
"""

import os
from pathlib import Path
from typing import Optional


def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not api_key or not isinstance(api_key, str):
        return False
    
    # Groq API keys typically start with 'gsk_'
    return api_key.strip().startswith('gsk_')


def validate_file(file_path: Path, allowed_extensions: list = ['.txt']) -> bool:
    """
    Validate if file exists and has allowed extension.
    
    Args:
        file_path: Path to file
        allowed_extensions: List of allowed file extensions
        
    Returns:
        True if valid, False otherwise
    """
    if not file_path.exists():
        return False
    
    return file_path.suffix.lower() in allowed_extensions


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def safe_get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Safely get environment variable.
    
    Args:
        key: Environment variable key
        default: Default value if not found
        
    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)