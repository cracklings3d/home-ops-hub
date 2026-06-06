"""
Qdrant vector store wrapper for RAG functionality.
"""
import uuid
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from .config import QDRANT_URL, EMBEDDING_DIMENSION


class VectorStore:
    """QdrantClient wrapper for vector operations."""

    def __init__(self, url: str = QDRANT_URL, dimension: int = EMBEDDING_DIMENSION):
        self.client = QdrantClient(url=url)
        self.dimension = dimension

    def create_collection(self, family_id: str) -> str:
        """
        Create a collection for a document family.
        
        Args:
            family_id: Unique identifier for the document family
            
        Returns:
            Collection name (format: family_{family_id})
        """
        collection_name = f"family_{family_id}"
        self.client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=self.dimension,
                distance=Distance.COSINE
            )
        )
        return collection_name

    def delete_document_chunks(self, collection_name: str, document_id: str) -> bool:
        """
        Delete all chunks associated with a document.
        
        Args:
            collection_name: Name of the collection
            document_id: Unique identifier for the document
            
        Returns:
            True if successful
        """
        self.client.delete(
            collection_name=collection_name,
            points_selector=[
                {
                    "filter": {
                        "must": [
                            {"key": "document_id", "match": {"value": document_id}}
                        ]
                    }
                }
            ]
        )
        return True

    def search(
        self,
        collection_name: str,
        query_vector: list[float],
        limit: int = 5,
        score_threshold: float = 0.7
    ) -> list[dict[str, Any]]:
        """
        Search for similar vectors in a collection.
        
        Args:
            collection_name: Name of the collection
            query_vector: The query embedding vector
            limit: Maximum number of results
            score_threshold: Minimum similarity score
            
        Returns:
            List of search results with metadata
        """
        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold
        )
        return [
            {
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            }
            for result in results
        ]

    def upsert_vectors(
        self,
        collection_name: str,
        vectors: list[tuple[str, list[float], dict]],
        document_id: str
    ) -> bool:
        """
        Insert vectors into a collection.
        
        Args:
            collection_name: Name of the collection
            vectors: List of (id, vector, metadata) tuples
            document_id: Document identifier for filtering
            
        Returns:
            True if successful
        """
        points = [
            {
                "id": vid,
                "vector": vec,
                "payload": {**meta, "document_id": document_id}
            }
            for vid, vec, meta in vectors
        ]
        self.client.upsert(collection_name=collection_name, points=points)
        return True


# Singleton instance
_vector_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    """Get or create the singleton VectorStore instance."""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store