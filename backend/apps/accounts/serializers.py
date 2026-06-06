from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Family, Membership, Profile


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ["id", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "avatar", "default_family"]
        read_only_fields = ["id"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    family_name = serializers.CharField(write_only=True, required=False, max_length=100)

    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "family_name"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        family_name = validated_data.pop("family_name", None)
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # Auto-create family and membership
        family_name = family_name or f"{user.username}'s Family"
        family = Family.objects.create(name=family_name)
        Membership.objects.create(user=user, family=family, role="admin")
        Profile.objects.create(user=user, default_family=family)
        user.default_family = family
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        attrs["user"] = user
        return attrs


class MeSerializer(serializers.ModelSerializer):
    family_id = serializers.SerializerMethodField()
    family_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "family_id", "family_name"]

    def get_family_id(self, obj):
        return str(obj.default_family_id) if obj.default_family else None

    def get_family_name(self, obj):
        return obj.default_family.name if obj.default_family else None
