from rest_framework import serializers
from .models import Document, DocumentVersion


class DocumentVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVersion
        fields = ["id", "file_url", "file_type", "version_number", "created_by", "created_at"]
        read_only_fields = ["id", "version_number", "created_at"]


class DocumentSerializer(serializers.ModelSerializer):
    versions = DocumentVersionSerializer(many=True, read_only=True)
    owner_email = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "id", "title", "file_url", "file_type", "owner", "owner_email",
            "family", "status", "vector_ids", "versions", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "owner", "status", "vector_ids", "created_at", "updated_at"]

    def get_owner_email(self, obj):
        return obj.owner.email if obj.owner else None

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    title = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return validated_data
