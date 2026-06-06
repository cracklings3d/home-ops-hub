"""
URL configuration for RAG vector store API.
"""
from django.urls import path

from .views import CollectionView, DocumentChunksView

urlpatterns = [
    path("collections/", CollectionView.as_view(), name="rag-collections"),
    path("collections/<str:document_id>/", DocumentChunksView.as_view(), name="rag-document-chunks"),
]