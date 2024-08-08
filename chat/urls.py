from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat_room_list, name="chat_room_list"),
    path("<int:pk>/", views.chat_room_detail, name="chat_room_detail"),
    path("private/", views.private_message_list, name="private_message_list"),
    path(
        "private/<str:username>/",
        views.private_message_detail,
        name="private_message_detail",
    ),
    path("logoutChat/", views.logoutChat, name="logoutChat"),
]
