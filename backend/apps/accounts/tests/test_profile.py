import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Family, Membership, Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_profile_created_on_user_creation(self):
        """Profile should be auto-created"""
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)

    def test_profile_avatar_optional(self):
        self.assertIsNone(self.user.profile.avatar)


class FamilyModelTest(TestCase):
    def test_family_creation(self):
        family = Family.objects.create(name="Test Family")
        self.assertEqual(family.name, "Test Family")
        self.assertIsNotNone(family.created_at)


class MembershipModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="memuser", email="mem@example.com", password="testpass123"
        )
        self.family = Family.objects.create(name="Mem Family")

    def test_membership_unique_per_family(self):
        Membership.objects.create(user=self.user, family=self.family, role="admin")
        with self.assertRaises(Exception):
            Membership.objects.create(user=self.user, family=self.family, role="member")

    def test_membership_role_default(self):
        m = Membership.objects.create(user=self.user, family=self.family)
        self.assertEqual(m.role, "member")


class MeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="meuser", email="me@example.com", password="testpass123"
        )

    def test_me_returns_user_info(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get("/api/auth/me/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["email"], "me@example.com")

    def test_me_unauthenticated(self):
        resp = self.client.get("/api/auth/me/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
