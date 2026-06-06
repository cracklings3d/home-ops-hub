"""
Serializers for user registration, login, and token refresh.
"""
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Family, Membership, Profile, User


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(
        write_only=True, min_length=8, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    def validate_email(self, value):
        return value.lower()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"].lower(),
            password=validated_data["password"],
        )
        # Auto-create family with user's name
        family = Family.objects.create(name=f"{user.username}'s Family")
        # Create membership as admin
        Membership.objects.create(user=user, family=family, role="admin")
        # Set default family
        user.default_family = family
        user.save()
        # Create profile
        Profile.objects.create(user=user, default_family=family)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer for user data."""

    class Meta:
        model = User
        fields = ["id", "username", "email"]
        read_only_fields = ["id", "username", "email"]


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        email = attrs["email"].lower()
        password = attrs["password"]
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        attrs["user"] = user
        return attrs


class TokenRefreshSerializer(serializers.Serializer):
    """Serializer for JWT token refresh."""
    refresh = serializers.CharField()


class FamilySerializer(serializers.ModelSerializer):
    """Serializer for Family model."""

    class Meta:
        model = Family
        fields = ["id", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model."""
    user = UserSerializer(read_only=True)
    default_family = FamilySerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user", "avatar", "default_family"]
        read_only_fields = ["id", "user"]


class MeSerializer(serializers.ModelSerializer):
    """Serializer for current user data with family info."""
    profile = ProfileSerializer(read_only=True)
    family_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "family_id", "profile"]

    def get_family_id(self, obj):
        if obj.default_family:
            return str(obj.default_family.id)
        return None