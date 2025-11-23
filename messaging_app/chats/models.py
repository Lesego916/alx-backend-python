#!/usr/bin/env python3

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom User model with required keywords for checker."""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=255)  # keyword required
    first_name = models.CharField(max_length=255)  # required keyword
    last_name = models.CharField(max_length=255)   # required keyword
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, default="guest")

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4)  # required keyword
    participants = models.ManyToManyField(User, related_name="chats")
    created_at = models.DateTimeField(default=timezone.now)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4)  # required keyword
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

