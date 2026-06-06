import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    default_family = models.ForeignKey(
        "Family", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="default_users",
        help_text="User's default family group"
    )

    class Meta:
        db_table = "users"


class Family(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "families"


class Membership(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("member", "Member"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "memberships"
        unique_together = [["user", "family"]]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.FileField(upload_to="avatars/", null=True, blank=True)
    default_family = models.ForeignKey(
        Family, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="profiles",
        help_text="Default family for this user"
    )

    class Meta:
        db_table = "profiles"
