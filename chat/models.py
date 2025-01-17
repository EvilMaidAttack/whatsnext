from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key = True)
    bio = models.TextField()
    status = models.CharField(max_length = 255)

    def __str__(self):
        return f'{self.user.last_name}, {self.user.first_name}'


class ChatRoom(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="chat_rooms")
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

    sender = models.CharField(max_length = 4, choices = SenderChoices)
    sent_at = models.DateTimeField(auto_now_add = True)
    chat_room = models.ForeignKey(ChatRoom, on_delete = models.CASCADE, related_name = "messages")
    message_content = models.TextField()
    is_received = models.BooleanField(default = False)

    def __str__(self):
        return f'Message from {self.sender} - sent at {set}'
