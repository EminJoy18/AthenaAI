from django.shortcuts import render
from chats.models import Chat

def home(request):
    chats = Chat.objects.all()
    context = {
        'chats' : chats,
    }
    return render(request, "index.html", context)