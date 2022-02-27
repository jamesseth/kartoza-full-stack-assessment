"""Django Admin Core app model."""
from django.contrib import admin   # noqa:F401
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models


class UserAdmin(BaseUserAdmin):
    """Custom admin user model."""

    ordering = ['id']
    list_display = ['email', 'name']


admin.site.register(models.User, UserAdmin)
