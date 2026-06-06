from django.db import migrations, models
import django.db.models.deletion
import uuid
import apps.documents.models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("file", models.FileField(blank=True, null=True, upload_to=apps.documents.models.document_upload_path)),
                ("file_url", models.URLField(blank=True, max_length=500, null=True)),
                ("file_type", models.CharField(default="pdf", max_length=50)),
                ("status", models.CharField(choices=[("processing", "Processing"), ("ready", "Ready"), ("failed", "Failed")], default="processing", max_length=20)),
                ("vector_ids", models.JSONField(blank=True, default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("family", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="documents", to="accounts.family")),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="documents", to="accounts.user")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="DocumentVersion",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("file", models.FileField(upload_to=apps.documents.models.document_upload_path)),
                ("file_url", models.URLField(blank=True, max_length=500, null=True)),
                ("file_type", models.CharField(max_length=50)),
                ("version_number", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="accounts.user")),
                ("document", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="versions", to="documents.document")),
            ],
            options={"ordering": ["-version_number"], "unique_together": {("document", "version_number")}},
        ),
    ]
