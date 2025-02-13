# users/managers.py
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from xrpl.wallet import generate_faucet_wallet
from xrpl.clients import JsonRpcClient


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)

        # Use provided wallet_address or leave it empty
        if 'wallet_address' not in extra_fields or not extra_fields['wallet_address']:
            # Leave it empty if not provided
            extra_fields['wallet_address'] = None

        user = self.model(username=username, email=email,
                          first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('profile_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Automatically generate a wallet ONLY for superusers if not provided
        if 'wallet_address' not in extra_fields or not extra_fields['wallet_address']:
            try:
                client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
                wallet = generate_faucet_wallet(client, debug=True)
                extra_fields['wallet_address'] = wallet.classic_address
                print(
                    f"Wallet created for superuser: {wallet.classic_address}")
                print(f"Seed (save this): {wallet.seed}")
            except Exception as e:
                print(f"Error creating wallet: {str(e)}")
                extra_fields['wallet_address'] = f'ADMIN_WALLET_{username}'

        return self.create_user(username, email, first_name, last_name, password, **extra_fields)
