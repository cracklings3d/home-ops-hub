"""
Tests for Consumable CRUD API endpoints.
"""
from decimal import Decimal
from django.utils import timezone

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User
from apps.assets.models import Asset
from ..models import Consumable, UsageRecord


class ConsumableViewTestCase(TestCase):
    """Test Consumable CRUD API."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="t@t.com", password="TestPass123!"
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_list_consumables_empty(self):
        """GET /api/consumables/ with no consumables returns 200 empty list."""
        resp = self.client.get("/api/consumables/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_consumable(self):
        """POST /api/consumables/ creates consumable and returns 201."""
        resp = self.client.post(
            "/api/consumables/",
            {
                "name": "HP 65 Ink",
                "recommended_brand": "HP",
                "current_stock": 5,
                "low_stock_threshold": 2,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["name"], "HP 65 Ink")
        self.assertIn("id", resp.data)

    def test_retrieve_consumable(self):
        """GET /api/consumables/{id}/ returns consumable details."""
        consumable = Consumable.objects.create(
            name="AA Battery",
            current_stock=10,
            created_by=self.user,
        )
        resp = self.client.get(f"/api/consumables/{consumable.id}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["name"], "AA Battery")

    def test_patch_consumable(self):
        """PATCH /api/consumables/{id}/ partially updates consumable."""
        consumable = Consumable.objects.create(
            name="AA Battery",
            current_stock=10,
            created_by=self.user,
        )
        resp = self.client.patch(
            f"/api/consumables/{consumable.id}/",
            {"current_stock": 5},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        consumable.refresh_from_db()
        self.assertEqual(consumable.current_stock, 5)

    def test_delete_soft(self):
        """DELETE /api/consumables/{id}/ soft-deletes (sets is_deleted=True)."""
        consumable = Consumable.objects.create(
            name="AA Battery",
            current_stock=10,
            created_by=self.user,
        )
        resp = self.client.delete(f"/api/consumables/{consumable.id}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        consumable.refresh_from_db()
        self.assertTrue(consumable.is_deleted)

    def test_low_stock_endpoint(self):
        """GET /api/consumables/low-stock/ returns only low-stock items."""
        Consumable.objects.create(
            name="HP Ink",
            current_stock=5,
            low_stock_threshold=2,
            created_by=self.user,
        )
        Consumable.objects.create(
            name="Battery",
            current_stock=1,
            low_stock_threshold=2,
            created_by=self.user,
        )
        resp = self.client.get("/api/consumables/low_stock/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["name"], "Battery")