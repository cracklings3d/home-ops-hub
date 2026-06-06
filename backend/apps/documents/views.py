import uuid
import minio_storage
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from .models import Document, DocumentVersion
from .serializers import DocumentSerializer, DocumentUploadSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def new_version(self, request, pk=None):
        doc = self.get_object()
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        # Upload to storage
        file_path = f"documents/{doc.id}/{file_obj.name}"
        from django.core.files.storage import default_storage
        saved_path = default_storage.save(file_path, file_obj)
        file_url = default_storage.url(saved_path)
        # Create version
        latest = doc.versions.first()
        version_num = (latest.version_number + 1) if latest else 1
        version = DocumentVersion.objects.create(
            document=doc,
            file=file_path,
            file_url=file_url,
            file_type=file_obj.content_type or "application/octet-stream",
            version_number=version_num,
            created_by=request.user,
        )
        # Update main doc
        doc.file = file_path
        doc.file_url = file_url
        doc.file_type = file_obj.content_type or "application/octet-stream"
        doc.save()
        from .serializers import DocumentVersionSerializer
        return Response(DocumentVersionSerializer(version).data)

    @action(detail=True, methods=["get"])
    def versions(self, request, pk=None):
        doc = self.get_object()
        from .serializers import DocumentVersionSerializer
        return Response(DocumentVersionSerializer(doc.versions.all(), many=True).data)
