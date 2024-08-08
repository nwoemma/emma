from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls", namespace="pages")),  # Main page URL
    path("accounts/", include("accounts.urls")),
    path("chat/", include("chat.urls")),
    path("patients/", include("patients.urls")),
    path("doctor/", include("doctor.urls")),
]

# Serving media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
