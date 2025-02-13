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
    wallet_address = models.CharField(
        max_length=255, unique=True, blank=True, null=True)
    token_balance = models.DecimalField(
        max_digits=18, decimal_places=8, default=0)
    profile_type = models.CharField(
        max_length=20, choices=PROFILE_TYPES, default='standard')
    activation_code = models.CharField(
        max_length=64, blank=True, null=True
    )
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        if not self.wallet_address:  # generate empty wallet address
            self.wallet_address = f'ADMIN_WALLET_{self.username}'
        super().save(*args, **kwargs)
