from django.db import models
from django.contrib import auth

# Create your models here.
class User(auth.models.User, auth.models.PermissionsMixin):
    """
    This model is only to override the __str__ function for User model
    The actual User model used by our project is the default User provided by Django
    """
    def __str__(self):
        return "@{}".format(self.username)
