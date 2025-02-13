# users/managers.py
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from xrpl.wallet import generate_faucet_wallet
from xrpl.clients import JsonRpcClient


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('L\'adresse email est obligatoire'))

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        # Configuration pour le superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('profile_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        # Création automatique d'un wallet pour le superuser si non fourni
        if 'wallet_address' not in extra_fields:
            try:
                client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
                wallet = generate_faucet_wallet(client, debug=True)
                extra_fields['wallet_address'] = wallet.classic_address
                print(
                    f"Wallet créé pour le superuser: {wallet.classic_address}")
                print(f"Seed (à sauvegarder): {wallet.seed}")
            except Exception as e:
                print(f"Erreur lors de la création du wallet: {str(e)}")
                extra_fields['wallet_address'] = 'ADMIN_WALLET_' + username

        return self.create_user(username, email, password, **extra_fields)
