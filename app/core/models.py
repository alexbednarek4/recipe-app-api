import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings
# This class provides methods that help create users
# It creates a new user model, sets and encrypts password,
# then saves the model and returns the user


def recipe_image_file_path(instance, filename):
    """Generate filepath for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/recipe/', filename)


class UserManager(BaseUserManager):
    # The **extra_fields == (...args) in JS
    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have an email address")
        # You can access the model that the manager is for by typing self.model
        # Essentially creating a new user model
        # and assigning it to the user variable
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # encrypt password
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email instead of username"""
    email = models.EmailField(
        # unique creating one user with one email
        max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # when we delete a user, what happens to tags
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    # Assign fields (db columns)
    # Each recipe assigned to one user so
    # we use foreign key
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # blank=True, field indicates blank string
    # easier for debugging
    link = models.CharField(max_length=255, blank=True)
    # Diff types of foreign keys in a db
    # Many recipes assigned to many ingredients
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    # ImageField (via Django) calls the recipe_image_file_path in background
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
