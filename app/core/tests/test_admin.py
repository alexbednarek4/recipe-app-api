# We will store all admin page tests
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    # Setup function run before every test run
    def setUp(self):
        # sets to self a client variable
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@alex.com',
            password='password123'
        )
        # Admin is logged into client
        # We then have a spare user to use for testing
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@alex.com',
            password='password123',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # Check resources lec 32
        url = reverse('admin:core_user_changelist')
        # Test client will perform HTTP get on the url
        res = self.client.get(url)
        # Assert contains checks that our response contains
        # a certain item
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # Reverse func will create a user like this:
        # /admin/core/user/id
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Testing that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
