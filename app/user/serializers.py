from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
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


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    # Adding validate command which is called when we validate our serializer
    # Making sure email and password are of CharField types

    def validate(self, attrs):
        """ Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            # this is how we acces context of request
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            message = _(
                'Unable to authenticate user with provided credentials.')
            raise serializers.ValidationError(message, code='authentication')
        # Set user in attributes which we return
        # Must return attributes you validate
        attrs['user'] = user
        return attrs
