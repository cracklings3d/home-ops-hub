"""
Root URL configuration for home-ops-hub.
"""
from django.urls import include, path

urlpatterns = [
    path("api/auth/", include("apps.accounts.urls")),
    path("api/assets/", include("apps.assets.urls")),
    path("api/consumables/", include("apps.consumables.urls")),
    path("api/documents/", include("apps.documents.urls")),
    path("api/rag/", include("apps.rag.urls")),
]