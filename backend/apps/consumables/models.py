import uuid
from django.db import models
from django.conf import settings


class ConsumableCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=20, default="pcs")

    class Meta:
        db_table = "consumable_categories"
        verbose_name_plural = "Consumable Categories"

    def __str__(self):
        return self.name


class Consumable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        ConsumableCategory, on_delete=models.SET_NULL, null=True, related_name="consumables"
    )
    brand = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=20, default="pcs")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    supplier = models.URLField(max_length=500, blank=True)
    purchase_url = models.URLField(max_length=500, blank=True)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consumables"
    )
    family = models.ForeignKey(
        "accounts.Family", on_delete=models.CASCADE, null=True, blank=True,
        related_name="consumables"
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "consumables"

    def __str__(self):
        return self.name


class ConsumableStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consumable = models.ForeignKey(
        Consumable, on_delete=models.CASCADE, related_name="stock_records"
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "consumable_stock"

    def __str__(self):
        return f"{self.consumable.name} x {self.quantity}"
