from django.db import models
from users.models import User
import uuid


class Task(models.Model):
    TASK_TYPES = (
        ('credit_dispute', 'Credit Dispute'),
        ('subscription_cancel', 'Subscription Cancellation'),
        ('license_renewal', 'License Renewal'),
        ('refund_request', 'Refund Request'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    blockchain_transaction_id = models.CharField(max_length=255, null=True)


class AIInteraction(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='ai_interactions')
    input_data = models.JSONField()
    output_data = models.JSONField()
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)


class ServiceProvider(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    api_endpoint = models.URLField()
    api_credentials = models.JSONField()
    service_type = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
