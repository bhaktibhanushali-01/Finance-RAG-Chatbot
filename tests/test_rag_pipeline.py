"""
Unit tests for RAG pipeline components.
"""

import unittest
from pathlib import Path
from src.embeddings import EmbeddingsManager
from src.utils import validate_api_key, validate_file


class TestEmbeddings(unittest.TestCase):
    """Test embeddings functionality."""
    
    def test_embeddings_singleton(self):
        """Test that embeddings manager returns same instance."""
        emb1 = EmbeddingsManager.get_embeddings()
        emb2 = EmbeddingsManager.get_embeddings()
        self.assertIs(emb1, emb2)


class TestUtils(unittest.TestCase):
    """Test utility functions."""
    
    def test_validate_api_key_valid(self):
        """Test API key validation with valid key."""
        self.assertTrue(validate_api_key("gsk_1234567890"))
    
    def test_validate_api_key_invalid(self):
        """Test API key validation with invalid key."""
        self.assertFalse(validate_api_key("invalid_key"))
        self.assertFalse(validate_api_key(""))
        self.assertFalse(validate_api_key(None))
    
    def test_validate_file_extension(self):
        """Test file validation."""
        # This test would need actual files to be meaningful
        # Placeholder for now
        pass


if __name__ == '__main__':
    unittest.main()