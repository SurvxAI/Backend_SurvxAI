# governance/models.py
from django.db import models
from users.models import User
import uuid


class Governance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    proposal_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20)
    voting_start = models.DateTimeField()
    voting_end = models.DateTimeField()
    total_votes = models.IntegerField(default=0)


class Vote(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='votes')
    proposal = models.ForeignKey(
        Governance, on_delete=models.CASCADE, related_name='votes')
    vote_weight = models.DecimalField(max_digits=18, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)
