"""
Custom User model with UUID primary key.
"""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Family(models.Model):
    """Family/group model for organizing users."""
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts_family"
        verbose_name = "family"
        verbose_name_plural = "families"

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom user model using UUID as primary key and email as login field.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    default_family = models.ForeignKey(
        Family,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_for_users",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "accounts_user"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email


class Membership(models.Model):
    """Membership model linking users to families with roles."""
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("member", "Member"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts_membership"
        verbose_name = "membership"
        verbose_name_plural = "memberships"
        unique_together = ["user", "family"]

    def __str__(self):
        return f"{self.user.email} - {self.family.name} ({self.role})"


class Profile(models.Model):
    """User profile with avatar and default family."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.FileField(upload_to="avatars/", null=True, blank=True)
    default_family = models.ForeignKey(
        Family,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_for_profiles",
    )

    class Meta:
        db_table = "accounts_profile"
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        return f"Profile of {self.user.email}"