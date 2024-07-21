from django.urls import path
from pages import views

app_name = "pages"

urlpatterns = [
    path('',views.home, name='home'),
    path('about',views.about,  name='about'),
    path('menu',views.menu, name='menu'),
]
