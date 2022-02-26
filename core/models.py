"""Custom user model implemetation to use an email as a username."""
from typing import Any
from typing import Union

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Create custom user manager for email addresses as the username."""

    def create_user(self, email: str,
                    password: Union[None, str] = None, **extra_fields: Any) -> Any:
        """
        Create a new user object.

        :param email: The email address of the user
        :param password: If a password is provided, it will be hashed and set on the user
        :return: A user instance
        """
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create a Django super user."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Implement a user model to support email addresses as a username."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
