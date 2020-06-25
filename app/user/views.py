from rest_framework import generics
from user.serializers import UserSerializer
# View that allows us to easily create an API using serializer


class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system"""
    serializer_class = UserSerializer
