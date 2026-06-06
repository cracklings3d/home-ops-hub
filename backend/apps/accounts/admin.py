"""
Django admin registration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Family, Membership, Profile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for custom User model."""
    list_display = ["username", "email", "is_staff", "is_active", "date_joined"]
    search_fields = ["username", "email"]
    ordering = ["-date_joined"]


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    """Admin for Family model."""
    list_display = ["id", "name", "created_at"]
    search_fields = ["name"]
    ordering = ["-created_at"]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """Admin for Membership model."""
    list_display = ["id", "user", "family", "role", "joined_at"]
    list_filter = ["role"]
    search_fields = ["user__email", "family__name"]
    ordering = ["-joined_at"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin for Profile model."""
    list_display = ["id", "user", "default_family"]
    search_fields = ["user__email"]
    ordering = ["-id"]