from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # Allows us to configure a few extra settings
        # within model serializer
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        # create func is created and validated data
        # (JSON data from post request)
        # is used to create user
        return get_user_model().objects.create_user(**validated_data)
