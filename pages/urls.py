from django.urls import path
from pages import views

app_name = "pages"

urlpatterns = [
    path('',views.home, name='home'),
    path('about',views.about,  name='about'),
    path('menu',views.menu, name='menu'),
    path('title/<str:page_name>/', views.page_title, name='page_title'),
]
