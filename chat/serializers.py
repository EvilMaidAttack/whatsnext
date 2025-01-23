from rest_framework import serializers

from .models import ChatRoom, Message, Profile, ChatExport

# TODO: When posting chat_room has to be defined, but it can be set from the url
class MessageSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'is_received']
        
    def create(self, validated_data):
        message = Message.objects.create(chat_room_id = self.context.get('chatroom_id'), **validated_data)
        return message


class ReceiveMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['is_received']


class ChatRoomDetailSerializer(serializers.ModelSerializer):
    messages = MessageSeriaizer(many = True)
    class Meta:
        model = ChatRoom
        fields = ['id', 'profile', 'chat_partner_name', 'is_active', 'created_at', 'updated_at', 'messages']

        
class ChatRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    class Meta:
        model = ChatRoom
        fields = ['id', 'profile', 'chat_partner_name', 'is_active', 'created_at', 'updated_at', 'last_message']
    
    def get_last_message(self, obj:ChatRoom):
        last_message : Message | None = obj.messages.order_by('-timestamp').first()
        if last_message:
            return {
                "sender": last_message.sender,
                "content": last_message.content,
                "timestamp": last_message.timestamp,
                "is_received": last_message.is_received,
            }
        else:
            return None
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user_id", 'bio', 'status']