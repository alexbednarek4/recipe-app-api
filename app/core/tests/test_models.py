from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
# Helper function for creating users in tests


def sample_user(email='test@alex.com', password='testpass'):
    """ Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Testing creation of user is successful"""
        email = 'test@alex.com'
        password = 'testPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Testing that the email for the new user is normalized"""
        email = 'test@ALEX.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        # Anything that we run in here should raise a
        # value error, if not, test will fail
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@alex.com',
            'test123'
        )
        # is_superuser is included in PermissionsMIxin
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ Test creating a tag and verifies """
        """that it creates correct string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        # Assert that when we convert our tag model to a string
        # it will give us the name
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)
