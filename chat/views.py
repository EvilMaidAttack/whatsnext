from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import ChatRoomSerializer, ChatRoomDetailSerializer, MessageSeriaizer, ReceiveMessageSerializer, ProfileSerializer
from .models import ChatRoom, Message, Profile

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
    
    def get_serializer_context(self):
        return {"chatroom_id": self.kwargs['chatroom_pk']}
    
    def get_queryset(self):
        return Message.objects.filter(chat_room_id = self.kwargs['chatroom_pk'])


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    
    @action(detail=False, methods=["GET", "PUT"])
    def me(self, request):
        profile = Profile.objects.get(user_id = request.user.id)
        if request.method == "GET":
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = ProfileSerializer(profile, data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data)