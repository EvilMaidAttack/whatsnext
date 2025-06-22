from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
import logging

from .serializers import ChatExportSerializer, ChatRoomSerializer, ChatRoomDetailSerializer, MessageSeriaizer, ReceiveMessageSerializer, ProfileSerializer
from .models import ChatExport, ChatRoom, Message, Profile
from .services.openai_service import get_ai_response

logger = logging.getLogger(__name__)

# Create your views here.
class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.prefetch_related('messages').all()
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return ChatRoomDetailSerializer
        else:
            return ChatRoomSerializer
    
    def get_serializer_context(self):
        return {'profile_id': self.request.user.id}

    def get_queryset(self):
        return ChatRoom.objects.filter(profile_id = self.request.user.id).prefetch_related('messages')
    


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
    
    @action(detail=False, methods=["post"], url_path="ai-response") 
    def generate_ai_response(self, request, chatroom_pk=None):
        # load the chatroom
        try:
            chatroom = ChatRoom.objects.get(id=chatroom_pk)
        except ChatRoom.DoesNotExist:
            return Response({'error': 'Chatroom not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # get all messages and order them from newest to oldest
        messages_queryset = self.get_queryset().order_by('-timestamp')

        # get ai response
        try:
            ai_response = get_ai_response(messages_queryset, model="gpt-4.1", history_length=10)
        except Exception as e:
            logger.exception("AI response generation failed")
            return Response({'error': str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # create new message
        ai_message = Message.objects.create(
            sender = "ai",
            content = ai_response,
            is_received = True,
            chat_room = chatroom
            )
        
        return Response(MessageSeriaizer(ai_message).data, status=status.HTTP_201_CREATED)




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
        

class ChatExportViewSet(ModelViewSet):
    serializer_class = ChatExportSerializer
    
    def get_queryset(self):
        return ChatExport.objects.filter(profile_id = self.request.user.id)

    def get_serializer_context(self):
        return {'profile_id': self.request.user.id}