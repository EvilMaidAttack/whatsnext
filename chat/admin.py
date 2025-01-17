from django.contrib import admin

from .models import Profile, ChatRoom, Message

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass