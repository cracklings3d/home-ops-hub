"""
Views for RAG vector store API.
"""
import uuid
from typing import Any

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .vector_store import get_vector_store
from .config import EMBEDDING_PROVIDER, EMBEDDING_URL


@method_decorator(csrf_exempt, name="dispatch")
class CollectionView(View):
    """API view for managing vector collections."""

    def get(self, request) -> JsonResponse:
        """
        Get list of collections or collection info.
        
        Returns:
            JSON response with collection information
        """
        vector_store = get_vector_store()
        try:
            collections = vector_store.client.get_collections()
            return JsonResponse({
                "status": "success",
                "collections": [
                    {"name": c.name, "vectors_count": getattr(c, "vectors_count", 0)}
                    for c in collections.collections
                ],
                "embedding_provider": EMBEDDING_PROVIDER,
                "embedding_url": EMBEDDING_URL
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

    def post(self, request) -> JsonResponse:
        """
        Create a new collection for a document family.
        
        Request body:
            - family_id: Unique identifier for the family
            
        Returns:
            JSON response with collection info
        """
        try:
            import json
            body = json.loads(request.body)
            family_id = body.get("family_id", str(uuid.uuid4()))
            
            vector_store = get_vector_store()
            collection_name = vector_store.create_collection(family_id)
            
            return JsonResponse({
                "status": "success",
                "family_id": family_id,
                "collection_name": collection_name
            }, status=201)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class DocumentChunksView(View):
    """API view for managing document chunks in vector store."""

    def delete(self, request, document_id: str) -> JsonResponse:
        """
        Delete all chunks for a document.
        
        Args:
            document_id: The document identifier
            
        Returns:
            JSON response confirming deletion
        """
        try:
            collection_name = request.GET.get("collection")
            if not collection_name:
                return JsonResponse({
                    "status": "error",
                    "message": "collection parameter is required"
                }, status=400)
            
            vector_store = get_vector_store()
            vector_store.delete_document_chunks(collection_name, document_id)
            
            return JsonResponse({
                "status": "success",
                "document_id": document_id,
                "message": "Chunks deleted"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)