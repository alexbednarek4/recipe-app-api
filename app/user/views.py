from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer
# View that allows us to easily create an API using serializer


class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create new auth token for user"""
    serializer_class = AuthTokenSerializer
    # Sets renderer class so we can view the endpoint in the browser
    # e.g. logging in via post in the browser
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
