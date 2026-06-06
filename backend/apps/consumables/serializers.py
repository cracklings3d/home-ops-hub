from rest_framework import serializers
from .models import ConsumableCategory, Consumable, ConsumableStock


class ConsumableCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumableCategory
        fields = ["id", "name", "description", "unit"]
        read_only_fields = ["id"]


class ConsumableStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumableStock
        fields = ["id", "consumable", "quantity", "location", "expiry_date", "recorded_at"]
        read_only_fields = ["id", "recorded_at"]


class ConsumableSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Consumable
        fields = [
            "id", "name", "category", "category_name", "brand", "model_number",
            "unit", "price", "supplier", "purchase_url", "notes",
            "owner", "family", "is_deleted", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "owner", "is_deleted", "created_at", "updated_at"]

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
