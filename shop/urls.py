from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('book/',views.book_table, name= 'book_table'),
    path('product_list', views.product_list, name='product_list'),    
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
]