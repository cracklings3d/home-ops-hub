from rest_framework.routers import DefaultRouter
from .views import ConsumableCategoryViewSet, ConsumableViewSet, ConsumableStockViewSet

router = DefaultRouter()
router.register("categories", ConsumableCategoryViewSet, basename="consumable-category")
router.register("stock", ConsumableStockViewSet, basename="consumable-stock")
router.register("", ConsumableViewSet, basename="consumable")
urlpatterns = router.urls
