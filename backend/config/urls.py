from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/assets/", include("apps.assets.urls")),
    path("api/documents/", include("apps.documents.urls")),
    path("api/consumables/", include("apps.consumables.urls")),
    path("api/maintenance/", include("apps.maintenance.urls")),
    path("api/rag/", include("apps.rag.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
