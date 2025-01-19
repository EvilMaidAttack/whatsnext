from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ['first_name__istartswith', 'last_name__istartswith', 'username__istartswith']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "first_name", "last_name"),
            },
        ),
    )