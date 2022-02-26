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

    def test_new_user_email_valid(self):
        """Test the parsed email is normilized."""
        email = 'email@EMAIL.COM'
        user = get_user_model().objects.create_user(email=email, password='test-pasword!')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test create user with invalid email."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test-pasword!')

    def test_create_new_super_user(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            email='test@email.com', password='test-pasword')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
