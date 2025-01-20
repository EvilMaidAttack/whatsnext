from rest_framework import serializers

from .models import ChatRoom, Message, Profile, ChatExport

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['profile', 'chat_partner_name', 'is_active', 'created_at', 'updated_at']