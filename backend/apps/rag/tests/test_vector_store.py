"""
Tests for vector store functionality.
"""
import unittest
from unittest.mock import MagicMock, patch

from apps.rag.vector_store import VectorStore


class TestVectorStore(unittest.TestCase):
    """Test cases for VectorStore class."""

    @patch("apps.rag.vector_store.QdrantClient")
    def test_create_collection(self, mock_qdrant_class):
        """Test collection creation."""
        mock_client = MagicMock()
        mock_qdrant_class.return_value = mock_client

        vector_store = VectorStore()
        collection_name = vector_store.create_collection("doc-123")

        self.assertEqual(collection_name, "family_doc-123")
        mock_client.recreate_collection.assert_called_once()

    @patch("apps.rag.vector_store.QdrantClient")
    def test_delete_document_chunks(self, mock_qdrant_class):
        """Test deleting document chunks."""
        mock_client = MagicMock()
        mock_qdrant_class.return_value = mock_client

        vector_store = VectorStore()
        result = vector_store.delete_document_chunks("family_doc-123", "doc-456")

        self.assertTrue(result)
        mock_client.delete.assert_called_once()

    @patch("apps.rag.vector_store.QdrantClient")
    def test_search(self, mock_qdrant_class):
        """Test vector search."""
        mock_client = MagicMock()
        mock_qdrant_class.return_value = mock_client

        # Mock search result
        mock_result = MagicMock()
        mock_result.id = "vec-1"
        mock_result.score = 0.95
        mock_result.payload = {"text": "sample"}
        mock_client.search.return_value = [mock_result]

        vector_store = VectorStore()
        results = vector_store.search("family_doc-123", [0.1] * 1536, limit=5)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "vec-1")
        self.assertEqual(results[0]["score"], 0.95)
        mock_client.search.assert_called_once()


if __name__ == "__main__":
    unittest.main()