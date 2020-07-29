from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
# Import our tag model
from core.models import Tag
# Tag serializer which we create to make tests pass after writing
# unit tests
from recipe.serializers import TagSerializer

# Url is in recipe app, using view set which appends action
# name to url
TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@alex.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        # Create sample tags, then make request
        Tag.objects.create(user=self.user, name='Vegas')
        Tag.objects.create(user=self.user, name='Jimmy')
        # Make GET request which should return our tags
        res = self.client.get(TAGS_URL)
        # Make query on model we expect to get
        # Makes sure tags are returned in reverse order based on name
        tags = Tag.objects.all().order_by('-name')
        # If we pass without saying many=True it will assume
        # we are trying to serialize a single object
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # res.data is data from response
        # Expect the returned data to equal serializer data
        # Should be reverse list of tags by name
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@alex.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='FruitBoss')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
