from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .serializers import ChatRoomSerializer, ChatRoomDetailSerializer, MessageSeriaizer, ReceiveMessageSerializer
from .models import ChatRoom, Message

# Create your views here.
class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.prefetch_related('messages').all()
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return ChatRoomDetailSerializer
        else:
            return ChatRoomSerializer


class MessageViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return ReceiveMessageSerializer
        else:
            return MessageSeriaizer
    
    # TODO: Add the chatroom_id to the context
    def get_serializer_context(self):
        return super().get_serializer_context()
    
    def get_queryset(self):
        return Message.objects.filter(chat_room_id = self.kwargs['chatroom_pk'])