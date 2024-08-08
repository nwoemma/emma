from django.db import models
from accounts.models import CustomUser


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    is_private = models.BooleanField(default=False)
    users = models.ManyToManyField(CustomUser, related_name="chat_rooms")

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"


class PrivateMessage(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}: {self.content[:20]}"
