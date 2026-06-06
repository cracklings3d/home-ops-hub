from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from .models import ConsumableCategory, Consumable, ConsumableStock
from .serializers import ConsumableCategorySerializer, ConsumableSerializer, ConsumableStockSerializer


class ConsumableCategoryViewSet(viewsets.ModelViewSet):
    queryset = ConsumableCategory.objects.all()
    serializer_class = ConsumableCategorySerializer


class ConsumableViewSet(viewsets.ModelViewSet):
    serializer_class = ConsumableSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Consumable.objects.filter(owner=user)
        # Filter out deleted unless explicitly requested
        if self.request.query_params.get("include_deleted") != "true":
            qs = qs.filter(is_deleted=False)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category_id=category)
        return qs

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class ConsumableStockViewSet(viewsets.ModelViewSet):
    queryset = ConsumableStock.objects.all()
    serializer_class = ConsumableStockSerializer

    def get_queryset(self):
        consumable_id = self.request.query_params.get("consumable")
        if consumable_id:
            return ConsumableStock.objects.filter(consumable_id=consumable_id)
        return ConsumableStock.objects.all()
