"""
URL configuration for consumables app.
"""
from rest_framework.routers import DefaultRouter

from .views import ConsumableViewSet

router = DefaultRouter()
router.register("", ConsumableViewSet, basename="consumable")

urlpatterns = router.urls