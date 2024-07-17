from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    # path('profile_edit/', views.profile_edit, name='profile_edit'),
]