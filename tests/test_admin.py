"""Admin site test suite."""
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Admin Site test cases."""

    def setUp(self):
        """Instantiate test dependencies."""
        self.client = Client()
        self.admin_user = (get_user_model().objects.create_superuser(
            email='admin@email.com', password='test_password'))
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='test_password')

    def test_for_users_listed(self):
        """Test users are listed on admin user page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
