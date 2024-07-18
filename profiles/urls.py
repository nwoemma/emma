from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "profiles"

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    path('profile_edit/', views.edit_profile, name='profile_edit'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)