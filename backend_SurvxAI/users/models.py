from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
import uuid


class User(AbstractUser):
    PROFILE_TYPES = (
        ('standard', 'Standard User'),
        ('admin', 'Administrator'),
        ('provider', 'Service Provider'),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    wallet_address = models.CharField(max_length=255, unique=True)
    token_balance = models.DecimalField(
        max_digits=18, decimal_places=8, default=0)
    profile_type = models.CharField(
        max_length=20, choices=PROFILE_TYPES, default='standard')

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email', 'wallet_address']
