from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


# Assign variable for recipe url
# reverse('app:identifier of url in app')
RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Return recipe detail URL"""
    # args is alist bc we may have more than one arg
    # for single url
    return reverse("recipe:recipe-detail", args=[recipe_id])


def sample_tag(user, name='Main course'):
    """Create and return sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinnamon'):
    """Create and return sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


# Sample recipe will allow us to create sample recipes


def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    # Having defaults, easier to test
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        "price": 5.00
    }
    # updates accepts dictionary
    # takes keys and update or creates if not there
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """ Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@alex.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        # '-id' order in which they were created
        recipes = Recipe.objects.all().order_by('-id')
        # want to return data as list, so many=True
        serializer = RecipeSerializer(recipes, many=True)
        # Want to make sure data matches serializer we created
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes for user"""
        user2 = get_user_model().objects.create_user(
            'other@alex.com',
            'password123'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)
        # make request
        res = self.client.get(RECIPE_URL)
        # filter recipes by authenticated user
        recipes = Recipe.objects.filter(user=self.user)
        # pass returned query set to serializer
        # Must make sure we get recipes back in list form
        # even if only one recipe
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """test viewing recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))
        # generate url to call
        url = detail_url(recipe.id)
        res = self.client.get(url)
        # assert serialized data
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
