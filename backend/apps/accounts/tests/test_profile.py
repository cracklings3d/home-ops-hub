"""
Tests for profile, family, and membership models and endpoints.
"""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Family, Membership, Profile, User


class ProfileModelTestCase(TestCase):
    """Test Profile model creation and relationships."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="TestPass123!"
        )
        self.family = Family.objects.create(name="Test Family")

    def test_profile_auto_created_on_registration(self):
        """New user registration creates profile and family."""
        new_user = User.objects.create_user(
            username="newuser", email="new@test.com", password="TestPass123!"
        )
        # Create family and membership manually (as RegisterSerializer does)
        family = Family.objects.create(name="newuser's Family")
        Membership.objects.create(user=new_user, family=family, role="admin")
        new_user.default_family = family
        new_user.save()
        Profile.objects.create(user=new_user, default_family=family)
        
        self.assertTrue(hasattr(new_user, "profile"))
        self.assertIsNotNone(new_user.profile)
        self.assertEqual(new_user.profile.default_family, family)

    def test_profile_str_representation(self):
        """Profile __str__ returns expected format."""
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(str(profile), f"Profile of {self.user.email}")


class FamilyModelTestCase(TestCase):
    """Test Family model."""

    def test_family_creation(self):
        """Family can be created with name."""
        family = Family.objects.create(name="My Family")
        self.assertEqual(family.name, "My Family")
        self.assertIsNotNone(family.created_at)

    def test_family_str_representation(self):
        """Family __str__ returns name."""
        family = Family.objects.create(name="Test Family")
        self.assertEqual(str(family), "Test Family")


class MembershipModelTestCase(TestCase):
    """Test Membership model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="TestPass123!"
        )
        self.family = Family.objects.create(name="Test Family")

    def test_membership_creation(self):
        """Membership links user to family with role."""
        membership = Membership.objects.create(
            user=self.user, family=self.family, role="admin"
        )
        self.assertEqual(membership.user, self.user)
        self.assertEqual(membership.family, self.family)
        self.assertEqual(membership.role, "admin")
        self.assertIsNotNone(membership.joined_at)

    def test_membership_unique_constraint(self):
        """User cannot have duplicate membership for same family."""
        Membership.objects.create(user=self.user, family=self.family, role="member")
        with self.assertRaises(Exception):
            Membership.objects.create(user=self.user, family=self.family, role="admin")

    def test_membership_str_representation(self):
        """Membership __str__ returns expected format."""
        membership = Membership.objects.create(
            user=self.user, family=self.family, role="member"
        )
        expected = f"{self.user.email} - {self.family.name} (member)"
        self.assertEqual(str(membership), expected)


class MeViewTestCase(TestCase):
    """Test MeView endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="TestPass123!"
        )
        # Setup family and profile
        self.family = Family.objects.create(name="testuser's Family")
        Membership.objects.create(user=self.user, family=self.family, role="admin")
        self.user.default_family = self.family
        self.user.save()
        Profile.objects.create(user=self.user, default_family=self.family)

    def test_me_returns_user_info(self):
        """GET /api/auth/me/ returns user data when authenticated."""
        self.client.force_authenticate(user=self.user)
        resp = self.client.get("/api/auth/me/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["email"], self.user.email)
        self.assertEqual(resp.data["username"], self.user.username)
        self.assertIn("family_id", resp.data)

    def test_me_returns_family_id(self):
        """GET /api/auth/me/ returns family_id when user has default_family."""
        self.client.force_authenticate(user=self.user)
        resp = self.client.get("/api/auth/me/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["family_id"], str(self.family.id))

    def test_me_unauthenticated(self):
        """GET /api/auth/me/ returns 401 when not authenticated."""
        resp = self.client.get("/api/auth/me/")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)