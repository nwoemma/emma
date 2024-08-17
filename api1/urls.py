from django.urls import path
from api1.views import HomeView, AboutView, ServicesView, ContactView

urlpatterns = [
    path('api/home/', HomeView.as_view(), name='api_home'),
    path('api/about/', AboutView.as_view(), name='api_about'),
    path('api/services/', ServicesView.as_view(), name='api_services'),
    path('api/contact/', ContactView.as_view(), name='api_contact'),
]
