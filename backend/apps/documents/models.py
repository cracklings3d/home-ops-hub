import uuid
from django.db import models
from django.conf import settings


def document_upload_path(instance, filename):
    return f"documents/{instance.document_id}/{filename}"


class Document(models.Model):
    STATUS_CHOICES = [
        ("processing", "Processing"),
        ("ready", "Ready"),
        ("failed", "Failed"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=document_upload_path, null=True, blank=True)
    file_url = models.URLField(max_length=500, null=True, blank=True)
    file_type = models.CharField(max_length=50, default="pdf")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents"
    )
    family = models.ForeignKey(
        "accounts.Family", on_delete=models.CASCADE, null=True, blank=True,
        related_name="documents"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="processing")
    vector_ids = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "documents"
        ordering = ["-created_at"]


class DocumentVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="versions"
    )
    file = models.FileField(upload_to=document_upload_path)
    file_url = models.URLField(max_length=500, null=True, blank=True)
    file_type = models.CharField(max_length=50)
    version_number = models.PositiveIntegerField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "document_versions"
        unique_together = [["document", "version_number"]]
        ordering = ["-version_number"]
