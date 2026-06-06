from django.contrib import admin
from .models import User, Family, Membership, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "username", "default_family", "is_active"]
    search_fields = ["email", "username"]


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "family", "role", "joined_at"]
    list_filter = ["role"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "default_family"]
