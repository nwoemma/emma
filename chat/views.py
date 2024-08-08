from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message, PrivateMessage, CustomUser
from .forms import MessageForm, PrivateMessageForm
from django.contrib.auth import logout


@login_required
def chat_room_list(request):
    chat_rooms = ChatRoom.objects.filter(users=request.user)
    return render(request, "chat/chat_room_list.html", {"chat_rooms": chat_rooms})


@login_required
def chat_room_detail(request, pk):
    chat_room = get_object_or_404(ChatRoom, pk=pk)
    messages = Message.objects.filter(chat_room=chat_room).order_by("timestamp")

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            Message.objects.create(
                user=request.user, chat_room=chat_room, content=content
            )
            return redirect("chat:chat_room_detail", pk=pk)
    else:
        form = MessageForm()

    return render(
        request,
        "chat/chat_room_detail.html",
        {"chat_room": chat_room, "messages": messages, "form": form},
    )


@login_required
def private_message_list(request):
    users = CustomUser.objects.exclude(username=request.user.username)
    return render(request, "chat/private_message_list.html", {"users": users})


@login_required
def private_message_detail(request, username):
    recipient = get_object_or_404(CustomUser, username=username)
    messages = PrivateMessage.objects.filter(
        sender=request.user, recipient=recipient
    ) | PrivateMessage.objects.filter(
        sender=recipient, recipient=request.user
    ).order_by(
        "timestamp"
    )

    if request.method == "POST":
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            PrivateMessage.objects.create(
                sender=request.user, recipient=recipient, content=content
            )
            return redirect("chat:private_message_detail", username=username)
    else:
        form = PrivateMessageForm()

    return render(
        request,
        "chat/private_message_detail.html",
        {"recipient": recipient, "messages": messages, "form": form},
    )


def logoutChat(request):
    # Clear chat-specific session data
    if "chat_data" in request.session:
        del request.session["chat_data"]
    return redirect("pages:authenticated_home")
