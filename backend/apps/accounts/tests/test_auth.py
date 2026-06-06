"""
Tests for accounts app authentication endpoints.
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import User


class AuthTestCase(TestCase):
    """Test register, login, refresh, and auth protection."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="TestPass123!"
        )

    def test_register_valid(self):
        """POST /api/auth/register/ with valid data returns 201 + tokens."""
        resp = self.client.post(
            "/api/auth/register/",
            {"username": "newuser", "email": "new@test.com", "password": "TestPass123!"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)
        self.assertEqual(resp.data["username"], "newuser")

    def test_register_invalid_password(self):
        """Short password returns 400."""
        resp = self.client.post(
            "/api/auth/register/",
            {"username": "newuser", "email": "new@test.com", "password": "short"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_valid(self):
        """POST /api/auth/login/ with correct credentials returns 200 + tokens."""
        resp = self.client.post(
            "/api/auth/login/",
            {"email": "test@test.com", "password": "TestPass123!"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)

    def test_login_wrong_password(self):
        """Wrong password returns 400."""
        resp = self.client.post(
            "/api/auth/login/",
            {"email": "test@test.com", "password": "WrongPass123!"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_valid(self):
        """POST /api/auth/refresh/ with valid refresh token returns new access."""
        resp = self.client.post(
            "/api/auth/login/",
            {"email": "test@test.com", "password": "TestPass123!"},
            format="json",
        )
        refresh_token = resp.data["refresh"]
        resp2 = self.client.post(
            "/api/auth/refresh/",
            {"refresh": refresh_token},
            format="json",
        )
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp2.data)

    def test_refresh_invalid_token(self):
        """Invalid refresh token returns 401."""
        resp = self.client.post(
            "/api/auth/refresh/",
            {"refresh": "invalid-token"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

