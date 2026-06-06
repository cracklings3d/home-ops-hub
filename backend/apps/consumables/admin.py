from django.contrib import admin
from .models import ConsumableCategory, Consumable, ConsumableStock


@admin.register(ConsumableCategory)
class ConsumableCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "unit"]


@admin.register(Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "brand", "price", "owner", "is_deleted"]
    list_filter = ["category", "is_deleted"]


@admin.register(ConsumableStock)
class ConsumableStockAdmin(admin.ModelAdmin):
    list_display = ["consumable", "quantity", "location", "expiry_date"]
