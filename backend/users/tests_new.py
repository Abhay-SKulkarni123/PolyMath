from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.models import EmailVerificationToken, PasswordResetToken, User

fake = Faker()


class PasswordChangeTests(APITestCase):
    """Test password change functionality"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", password="OldPass123!", first_name="Test", last_name="User"
        )

        # Get tokens
        login_url = reverse("login")
        login_data = {"email": "test@example.com", "password": "OldPass123!"}
        login_response = self.client.post(login_url, login_data, format="json")
        self.access_token = login_response.data["tokens"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_password_change_success(self):
        """Test successful password change"""
        url = reverse("password-change")
        data = {"old_password": "OldPass123!", "new_password": "NewPass456!", "confirm_new_password": "NewPass456!"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["error"])

        # Verify new password works
        self.client.credentials()
        login_data = {"email": "test@example.com", "password": "NewPass456!"}
        login_response = self.client.post(reverse("login"), login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_password_change_wrong_old_password(self):
        """Test password change fails with wrong old password"""
        url = reverse("password-change")
        data = {"old_password": "WrongPass123!", "new_password": "NewPass456!", "confirm_new_password": "NewPass456!"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data["error"])

    def test_password_change_password_mismatch(self):
        """Test password change fails with mismatched new passwords"""
        url = reverse("password-change")
        data = {"old_password": "OldPass123!", "new_password": "NewPass456!", "confirm_new_password": "DifferentPass789!"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data["error"])

    def test_password_change_unauthorized(self):
        """Test password change without auth fails"""
        self.client.credentials()
        url = reverse("password-change")
        data = {"old_password": "OldPass123!", "new_password": "NewPass456!", "confirm_new_password": "NewPass456!"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PasswordResetTests(APITestCase):
    """Test password reset flow"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", password="TestPass123!", first_name="Test", last_name="User"
        )

    def test_password_reset_request_success(self):
        """Test password reset request"""
        url = reverse("password-reset-request")
        data = {"email": "test@example.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["error"])

        # Verify token was created
        self.assertTrue(PasswordResetToken.objects.filter(user=self.user).exists())

    def test_password_reset_request_nonexistent_email(self):
        """Test password reset request with non-existent email"""
        url = reverse("password-reset-request")
        data = {"email": "nonexistent@example.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["error"])

    def test_password_reset_confirm_success(self):
        """Test successful password reset"""
        # Create reset token
        expires_at = timezone.now() + timedelta(hours=1)
        reset_token = PasswordResetToken.objects.create(user=self.user, expires_at=expires_at)

        url = reverse("password-reset-confirm")
        data = {"token": str(reset_token.token), "new_password": "NewPass456!", "confirm_new_password": "NewPass456!"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["error"])

        # Verify new password works
        login_data = {"email": "test@example.com", "password": "NewPass456!"}
        login_response = self.client.post(reverse("login"), login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_password_reset_confirm_invalid_token(self):
        """Test password reset with invalid token"""
        url = reverse("password-reset-confirm")
        data = {
            "token": "00000000-0000-0000-0000-000000000000",
            "new_password": "NewPass456!",
            "confirm_new_password": "NewPass456!",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data["error"])

    def test_password_reset_confirm_expired_token(self):
        """Test password reset with expired token"""
        # Create expired token
        expires_at = timezone.now() - timedelta(hours=1)
        reset_token = PasswordResetToken.objects.create(user=self.user, expires_at=expires_at)

        url = reverse("password-reset-confirm")
        data = {"token": str(reset_token.token), "new_password": "NewPass456!", "confirm_new_password": "NewPass456!"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data["error"])


class EmailVerificationTests(APITestCase):
    """Test email verification flow"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", password="TestPass123!", first_name="Test", last_name="User", is_email_verified=False
        )

    def test_email_verification_success(self):
        """Test successful email verification"""
        # Create verification token
        expires_at = timezone.now() + timedelta(hours=24)
        verification_token = EmailVerificationToken.objects.create(user=self.user, expires_at=expires_at)

        url = reverse("email-verify")
        data = {"token": str(verification_token.token)}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["error"])

        # Verify user is now verified
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_email_verified)

    def test_email_verification_invalid_token(self):
        """Test email verification with invalid token"""
        url = reverse("email-verify")
        data = {"token": "00000000-0000-0000-0000-000000000000"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data["error"])

    def test_email_verification_expired_token(self):
        """Test email verification with expired token"""
        # Create expired token
        expires_at = timezone.now() - timedelta(hours=1)
        verification_token = EmailVerificationToken.objects.create(user=self.user, expires_at=expires_at)

        url = reverse("email-verify")
        data = {"token": str(verification_token.token)}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data["error"])

    def test_email_verification_reuse_token(self):
        """Test that verification token can only be used once"""
        # Create and use token
        expires_at = timezone.now() + timedelta(hours=24)
        verification_token = EmailVerificationToken.objects.create(user=self.user, expires_at=expires_at)

        url = reverse("email-verify")
        data = {"token": str(verification_token.token)}

        # First use
        response1 = self.client.post(url, data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        # Second use should fail
        response2 = self.client.post(url, data, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


class HealthCheckTests(APITestCase):
    """Test health check endpoint"""

    def test_health_check(self):
        """Test health check returns healthy status"""
        url = reverse("health-check")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "healthy")
        self.assertIn("timestamp", response.data)
