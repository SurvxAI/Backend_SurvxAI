# blockchain/models.py
from django.db import models
from users.models import User
import uuid


class TokenTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('stake', 'Stake'),
        ('unstake', 'Unstake'),
        ('payment', 'Payment'),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='token_transactions')
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPES)
    blockchain_hash = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class SmartContract(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    contract_address = models.CharField(max_length=255, unique=True)
    contract_type = models.CharField(max_length=50)
    abi = models.JSONField()
    status = models.BooleanField(default=True)


class UserStake(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='stakes')
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    stake_date = models.DateTimeField(auto_now_add=True)
    unlock_date = models.DateTimeField()
    status = models.CharField(max_length=20)
