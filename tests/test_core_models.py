"""TestCases for Custom user model."""
from django.contrib.auth import get_user_model
from django.test import TestCase


class TestDataModels(TestCase):
    """Test custom user models."""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an emails succeeds."""
        email = 'email.email.com'
        password = 'TEST_PASSWORD'

        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
