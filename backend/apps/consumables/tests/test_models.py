import uuid
from django.test import TestCase
from apps.accounts.models import User
from .models import ConsumableCategory, Consumable, ConsumableStock


class ConsumableCategoryTest(TestCase):
    def test_create_category(self):
        cat = ConsumableCategory.objects.create(name="Filters", unit="pcs")
        self.assertEqual(cat.name, "Filters")

    def test_category_unique_name(self):
        ConsumableCategory.objects.create(name="Oil")
        with self.assertRaises(Exception):
            ConsumableCategory.objects.create(name="Oil")


class ConsumableTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="consuser", email="cons@example.com", password="testpass123"
        )

    def test_create_consumable(self):
        c = Consumable.objects.create(name="Oil Filter", owner=self.user)
        self.assertEqual(c.name, "Oil Filter")
        self.assertFalse(c.is_deleted)

    def test_soft_delete(self):
        c = Consumable.objects.create(name="To Delete", owner=self.user)
        c.is_deleted = True
        c.save()
        self.assertTrue(Consumable.objects.filter(id=c.id, is_deleted=True).exists())


class ConsumableStockTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="stockuser", email="stock@example.com", password="testpass123"
        )
        self.c = Consumable.objects.create(name="Filter", owner=self.user)

    def test_create_stock_record(self):
        s = ConsumableStock.objects.create(consumable=self.c, quantity=5)
        self.assertEqual(float(s.quantity), 5.0)
