from django.db import models
from django.conf import settings
import uuid

# Create your models here.
def user_upload_path(instance, filename):
    foldername = f'{instance.profile.user.id}_{instance.profile.user.username.split('@')[0]}'
    return f'chat_exports/{foldername}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key = True)
    bio = models.TextField()
    status = models.CharField(max_length = 255)

    def __str__(self):
        return f'{self.user.last_name}, {self.user.first_name}'
    
    def first_name(self):
        return self.user.first_name
    
    def last_name(self):
        return self.user.last_name


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="chat_rooms")
    chat_export = models.OneToOneField("ChatExport", on_delete = models.SET_NULL, 
                                       null = True, blank = True, related_name = "chat_room")
    chat_partner_name = models.CharField(max_length = 50)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'Chat of user {self.profile} created at {self.created_at}'


class Message(models.Model):
    class SenderChoices(models.TextChoices):
        profile = "user", "User"
        ai = "ai", "AI"

    chat_room = models.ForeignKey(ChatRoom, on_delete = models.CASCADE, related_name = "messages")
    sender = models.CharField(max_length = 4, choices = SenderChoices)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    is_received = models.BooleanField(default = False)

    def __str__(self):
        return f'Message from {self.sender} - sent at {self.timestamp}'
    

class ChatExport(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = "chat_exports")
    export = models.FileField(upload_to = user_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'Chat export by {self.profile} on {self.uploaded_at}'

