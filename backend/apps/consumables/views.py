"""
Views for Consumable CRUD API and related endpoints.
"""
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Consumable, UsageRecord
from .serializers import (
    ConsumableListSerializer,
    ConsumableSerializer,
    UsageRecordSerializer,
)


class ConsumableViewSet(viewsets.ModelViewSet):
    """
    CRUD viewset for Consumable model.
    """
    serializer_class = ConsumableSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["family"]

    def get_queryset(self):
        return Consumable.objects.filter(is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def list(self, request, *args, **kwargs):
        """Override list to use lightweight serializer."""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ConsumableListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ConsumableListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="usage-history")
    def usage_history(self, request, pk=None):
        """GET /consumables/{id}/usage-history/ - list usage records for consumable."""
        consumable = self.get_object()
        records = UsageRecord.objects.filter(consumable=consumable)
        serializer = UsageRecordSerializer(records, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="record-usage")
    def record_usage(self, request, pk=None):
        """POST /consumables/{id}/record-usage/ - record consumable usage."""
        consumable = self.get_object()

        quantity = request.data.get("quantity", 1)
        replaced_at = request.data.get("replaced_at")
        cost = request.data.get("cost")
        notes = request.data.get("notes", "")
        asset_id = request.data.get("asset")

        if not replaced_at:
            return Response(
                {"replaced_at": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update stock
        consumable.current_stock = F("current_stock") - quantity
        consumable.save(update_fields=["current_stock", "updated_at"])
        consumable.refresh_from_db()

        # Create usage record
        record = UsageRecord.objects.create(
            consumable=consumable,
            asset_id=asset_id,
            quantity=quantity,
            replaced_at=replaced_at,
            cost=cost,
            notes=notes,
            created_by=request.user,
        )
        serializer = UsageRecordSerializer(record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        """GET /consumables/low-stock/ - list consumables below threshold."""
        queryset = Consumable.objects.filter(
            is_deleted=False,
            current_stock__lte=F("low_stock_threshold"),
        )
        serializer = ConsumableListSerializer(queryset, many=True)
        return Response(serializer.data)