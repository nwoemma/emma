from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from chat.models import ChatRoom, Message, PrivateMessage
from accounts.models import CustomUser
from .serializers import ChatRoomSerializer, MessageSerializer, PrivateMessageSerializer, UserSerializer

class ChatRoomListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chat_rooms = ChatRoom.objects.filter(users=request.user)
        serializer = ChatRoomSerializer(chat_rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChatRoomDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        chat_room = ChatRoom.objects.get(pk=pk)
        messages = Message.objects.filter(chat_room=chat_room).order_by("timestamp")
        message_serializer = MessageSerializer(messages, many=True)
        return Response({
            'chat_room': ChatRoomSerializer(chat_room).data,
            'messages': message_serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, pk):
        chat_room = ChatRoom.objects.get(pk=pk)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, chat_room=chat_room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PrivateMessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.exclude(username=request.user.username)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PrivateMessageDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        recipient = CustomUser.objects.get(username=username)
        messages = PrivateMessage.objects.filter(
            sender=request.user, recipient=recipient
        ) | PrivateMessage.objects.filter(
            sender=recipient, recipient=request.user
        ).order_by("timestamp")
        serializer = PrivateMessageSerializer(messages, many=True)
        return Response({
            'recipient': UserSerializer(recipient).data,
            'messages': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, username):
        recipient = CustomUser.objects.get(username=username)
        serializer = PrivateMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, recipient=recipient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Clear chat-specific session data
        if "chat_data" in request.session:
            del request.session["chat_data"]
        return Response({"detail": "Successfully logged out of chat."}, status=status.HTTP_200_OK)
