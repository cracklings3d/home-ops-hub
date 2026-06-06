"""
Consumable and UsageRecord models.
"""
import uuid

from django.conf import settings
from django.db import models


class ConsumableFamily(models.Model):
    """Family/category for consumables (e.g. printer ink, batteries)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        db_table = "consumables_family"
        ordering = ["sort_order", "name"]
        verbose_name = "consumable family"
        verbose_name_plural = "consumable families"

    def __str__(self):
        return self.name


class Consumable(models.Model):
    """Consumable item model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    compatible_devices = models.JSONField(default=list, blank=True)
    recommended_brand = models.CharField(max_length=100, blank=True, null=True)
    estimated_lifetime = models.CharField(max_length=100, blank=True, null=True)
    replacement_cycle = models.CharField(max_length=100, blank=True, null=True)
    current_stock = models.IntegerField(default=1)
    low_stock_threshold = models.IntegerField(default=1)
    purchase_link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)
    family = models.ForeignKey(
        ConsumableFamily,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="consumables",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consumables",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = "consumables_consumable"
        ordering = ["-created_at"]
        verbose_name = "consumable"
        verbose_name_plural = "consumables"

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.current_stock <= self.low_stock_threshold


class UsageRecord(models.Model):
    """Record of consumable usage/replacement."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consumable = models.ForeignKey(
        Consumable,
        on_delete=models.CASCADE,
        related_name="usage_records",
    )
    asset = models.ForeignKey(
        "assets.Asset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="consumable_usages",
    )
    quantity = models.IntegerField(default=1)
    replaced_at = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consumable_usages",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = "consumables_usagerecord"
        ordering = ["-replaced_at"]
        verbose_name = "usage record"
        verbose_name_plural = "usage records"

    def __str__(self):
        return f"{self.consumable.name} - {self.replaced_at}"