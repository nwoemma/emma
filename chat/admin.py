from django.contrib import admin
from .models import ChatRoom, Message, PrivateMessage


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("users",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("user", "chat_room", "content", "timestamp")
    search_fields = ("user__username", "content")
    list_filter = ("chat_room", "timestamp")
    date_hierarchy = "timestamp"


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "content", "timestamp")
    search_fields = ("sender__username", "recipient__username", "content")
    list_filter = ("timestamp",)
    date_hierarchy = "timestamp"
