"""
Django admin registration for consumables app.
"""
from django.contrib import admin

from .models import Consumable, ConsumableFamily, UsageRecord


@admin.register(ConsumableFamily)
class ConsumableFamilyAdmin(admin.ModelAdmin):
    list_display = ["name", "icon", "color", "sort_order"]
    ordering = ["sort_order", "name"]


@admin.register(Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    list_display = ["name", "recommended_brand", "current_stock", "low_stock_threshold", "family", "created_by", "created_at"]
    list_filter = ["family", "is_deleted"]
    search_fields = ["name", "recommended_brand"]
    ordering = ["-created_at"]


@admin.register(UsageRecord)
class UsageRecordAdmin(admin.ModelAdmin):
    list_display = ["consumable", "asset", "quantity", "replaced_at", "cost", "created_by"]
    list_filter = ["consumable", "replaced_at"]
    search_fields = ["consumable__name"]
    ordering = ["-replaced_at"]