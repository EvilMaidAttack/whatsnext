from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .serializers import ChatRoomSerializer
from .models import ChatRoom

# Create your views here.
class ChatRoomViewSet(ModelViewSet):
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.all()