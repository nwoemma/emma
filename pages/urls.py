from django.urls import path
from pages import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),  # This should be publicly accessible
    path("about", views.about, name="about"),
    path("services", views.services, name="services"),
    path("contact", views.contact, name="contact"),
    path("authenticated_home/", views.authenticated_home, name="authenticated_home"),
]


handler404 = "pages.views.custom_404"
