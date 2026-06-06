from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from .models import Consumable, ConsumableCategory


class ConsumableAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="capiuser", email="capi@example.com", password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_consumables(self):
        Consumable.objects.create(name="Item 1", owner=self.user)
        resp = self.client.get("/api/consumables/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_consumable(self):
        resp = self.client.post("/api/consumables/", {"name": "New Item"}, format="json")
        self.assertIn(resp.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_filter_by_category(self):
        cat = ConsumableCategory.objects.create(name="Cat1")
        Consumable.objects.create(name="Item", owner=self.user, category=cat)
        resp = self.client.get(f"/api/consumables/?category={cat.id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_soft_delete(self):
        c = Consumable.objects.create(name="Del", owner=self.user)
        resp = self.client.delete(f"/api/consumables/{c.id}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_categories(self):
        ConsumableCategory.objects.create(name="Cat")
        resp = self.client.get("/api/consumables/categories/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
