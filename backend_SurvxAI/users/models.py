from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
import random


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
    activation_code_created = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        if not self.wallet_address:  # generate empty wallet address
            self.wallet_address = f'ADMIN_WALLET_{self.username}'
        super().save(*args, **kwargs)

    def generate_activation_code(self):
        """Génère un code d'activation à 6 chiffres"""
        code = ''.join(random.choices('0123456789', k=6))
        self.activation_code = code
        self.activation_code_created = timezone.now()
        self.save()
        return code

    def send_activation_email(self):
        """Envoie l'email d'activation"""
        subject = 'Activez votre compte'
        code = self.generate_activation_code()

        # Création du contenu HTML de l'email
        html_message = render_to_string('emails/activation_email.html', {
            'user': self,
            'code': code,
            'domain': settings.SITE_DOMAIN,
        })

        # Version texte de l'email
        plain_message = strip_tags(html_message)

        # Envoi de l'email
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            html_message=html_message,
            fail_silently=False,
        )
