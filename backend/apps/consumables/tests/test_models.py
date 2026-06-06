"""
Tests for Consumable and UsageRecord models.
"""
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import User
from ..models import Consumable, ConsumableFamily, UsageRecord


class ConsumableModelTestCase(TestCase):
    """Test Consumable and ConsumableFamily models."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="t@t.com", password="TestPass123!"
        )

    def test_create_consumable_family(self):
        """ConsumableFamily can be created with name."""
        family = ConsumableFamily.objects.create(name="Printer Ink")
        self.assertEqual(str(family), "Printer Ink")

    def test_create_consumable(self):
        """Consumable can be created with required fields."""
        consumable = Consumable.objects.create(
            name="HP 65 Ink",
            recommended_brand="HP",
            current_stock=5,
            low_stock_threshold=2,
            created_by=self.user,
        )
        self.assertEqual(str(consumable), "HP 65 Ink")
        self.assertEqual(consumable.current_stock, 5)
        self.assertFalse(consumable.is_deleted)
        self.assertFalse(consumable.is_low_stock)

    def test_consumable_is_low_stock(self):
        """Consumable.is_low_stock returns True when stock <= threshold."""
        consumable = Consumable.objects.create(
            name="HP 65 Ink",
            current_stock=2,
            low_stock_threshold=2,
            created_by=self.user,
        )
        self.assertTrue(consumable.is_low_stock)

        consumable.current_stock = 3
        self.assertFalse(consumable.is_low_stock)

    def test_usage_record(self):
        """UsageRecord can be created linked to consumable."""
        consumable = Consumable.objects.create(
            name="AA Battery",
            current_stock=10,
            created_by=self.user,
        )
        replaced_at = timezone.now()
        record = UsageRecord.objects.create(
            consumable=consumable,
            quantity=2,
            replaced_at=replaced_at,
            cost=Decimal("5.99"),
            notes="Replaced in remote control",
            created_by=self.user,
        )
        self.assertEqual(record.consumable, consumable)
        self.assertEqual(record.quantity, 2)
        self.assertIn("AA Battery", str(record))