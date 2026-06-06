import uuid
from django.test import TestCase
from apps.accounts.models import User
from .models import Document, DocumentVersion


class DocumentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="docuser", email="doc@example.com", password="testpass123"
        )

    def test_document_creation(self):
        doc = Document.objects.create(
            title="Test Manual", owner=self.user, file_type="pdf"
        )
        self.assertEqual(doc.title, "Test Manual")
        self.assertEqual(doc.status, "processing")
        self.assertIsNotNone(doc.id)

    def test_document_default_type(self):
        doc = Document.objects.create(title="Test", owner=self.user)
        self.assertEqual(doc.file_type, "pdf")


class DocumentVersionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="veruser", email="ver@example.com", password="testpass123"
        )
        self.doc = Document.objects.create(
            title="Manual v1", owner=self.user, file_type="pdf"
        )

    def test_version_creation(self):
        ver = DocumentVersion.objects.create(
            document=self.doc,
            file_type="pdf",
            version_number=1,
            created_by=self.user,
        )
        self.assertEqual(ver.version_number, 1)

    def test_version_unique_per_document(self):
        DocumentVersion.objects.create(
            document=self.doc, file_type="pdf", version_number=1, created_by=self.user
        )
        with self.assertRaises(Exception):
            DocumentVersion.objects.create(
                document=self.doc, file_type="pdf", version_number=1, created_by=self.user
            )
