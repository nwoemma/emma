from django.urls import path
from .views import ChatRoomListView, ChatRoomDetailView, PrivateMessageListView, PrivateMessageDetailView, LogoutChatView

urlpatterns = [
    path('chat_rooms/', ChatRoomListView.as_view(), name='api_chat_room_list'),
    path('chat_rooms/<int:pk>/', ChatRoomDetailView.as_view(), name='api_chat_room_detail'),
    path('private_messages/', PrivateMessageListView.as_view(), name='api_private_message_list'),
    path('private_messages/<str:username>/', PrivateMessageDetailView.as_view(), name='api_private_message_detail'),
    path('logout/', LogoutChatView.as_view(), name='api_logout_chat'),
]
