"""
Serializers for Consumable and UsageRecord models.
"""
from rest_framework import serializers

from .models import Consumable, ConsumableFamily, UsageRecord


class ConsumableFamilySerializer(serializers.ModelSerializer):
    """Serializer for ConsumableFamily model."""
    class Meta:
        model = ConsumableFamily
        fields = ["id", "name", "icon", "color", "sort_order"]
        read_only_fields = ["id"]


class UsageRecordSerializer(serializers.ModelSerializer):
    """Serializer for UsageRecord model."""
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    asset_name = serializers.CharField(source="asset.name", read_only=True, allow_null=True)

    class Meta:
        model = UsageRecord
        fields = [
            "id",
            "consumable",
            "asset",
            "asset_name",
            "quantity",
            "replaced_at",
            "cost",
            "notes",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]


class ConsumableSerializer(serializers.ModelSerializer):
    """Serializer for Consumable model with read-only created_by and timestamps."""
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    family_detail = ConsumableFamilySerializer(source="family", read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Consumable
        fields = [
            "id",
            "name",
            "compatible_devices",
            "recommended_brand",
            "estimated_lifetime",
            "replacement_cycle",
            "current_stock",
            "low_stock_threshold",
            "purchase_link",
            "notes",
            "family",
            "family_detail",
            "created_by",
            "created_at",
            "updated_at",
            "is_deleted",
            "is_low_stock",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at", "is_deleted"]


class ConsumableListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Consumable
        fields = [
            "id",
            "name",
            "recommended_brand",
            "current_stock",
            "low_stock_threshold",
            "is_low_stock",
        ]