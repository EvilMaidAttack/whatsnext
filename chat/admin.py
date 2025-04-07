from django.contrib import admin

from .models import Profile, ChatRoom, Message, ChatExport

# Register your models here.
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']
    autocomplete_fields = ['user']
    list_select_related = ['user']
    list_display = ['first_name', 'last_name', 'bio', 'status']


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'chat_partner_name', 'is_active', 'created_at', 'updated_at']
    autocomplete_fields = ['profile']
    inlines = [MessageInline]


@admin.register(ChatExport)
class ChatExportAdmin(admin.ModelAdmin):
    autocomplete_fields = ['profile']
    list_display = ['export', 'profile', 'uploaded_at']


