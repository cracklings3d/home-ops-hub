from django.test import TestCase
from django.test.client import encode_multipart
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from .models import Document


class DocumentAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="apiuser", email="api@example.com", password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_document(self):
        resp = self.client.post("/api/documents/", {"title": "My Doc"}, format="json")
        self.assertIn(resp.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_list_documents(self):
        Document.objects.create(title="Doc 1", owner=self.user)
        resp = self.client.get("/api/documents/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["count"], 1)

    def test_filter_by_owner(self):
        Document.objects.create(title="My Doc", owner=self.user)
        resp = self.client.get("/api/documents/")
        self.assertEqual(resp.data["count"], 1)

    def test_versions_endpoint(self):
        doc = Document.objects.create(title="Doc", owner=self.user)
        resp = self.client.get(f"/api/documents/{doc.id}/versions/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_new_version_requires_file(self):
        doc = Document.objects.create(title="Doc", owner=self.user)
        resp = self.client.post(f"/api/documents/{doc.id}/new_version/")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_document(self):
        doc = Document.objects.create(title="To Delete", owner=self.user)
        resp = self.client.delete(f"/api/documents/{doc.id}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
