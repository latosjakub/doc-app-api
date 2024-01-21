"""
Database models.
"""

from django.db import models
from django.contrib.auth. models import (
    PermissionsMixin,
    AbstractBaseUser,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    """Default UserMangager."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return user."""
        if not email:
            raise ValueError('User mus have an email.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Base User Model"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_it = models.BooleanField(default=False)
    is_mana = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()
