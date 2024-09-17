from django.urls import path

from .views import FoodItemDetail, FoodItemListCreate, OrderListCreate

urlpatterns = [
    path("fooditems/", FoodItemListCreate.as_view(), name="fooditem-list-create"),
    path("fooditems/<int:pk>/", FoodItemDetail.as_view(), name="fooditem-detail"),
    path("orders/", OrderListCreate.as_view(), name="order-list-create"),
    path("fooditems/<int:pk>/", FoodItemDetail.as_view(), name="fooditem-detail"),
]
