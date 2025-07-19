from typing import override
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    """
    Custom User Model extending Django's AbstractUser.
    This model satisfies all requirements from the "User" entity specification.
    """
    username=None
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True, editable=False)
    first_name = models.CharField(_("First Name"), max_length=150, blank=False, null=False)
    last_name = models.CharField(_("Last Name"), max_length=150, blank=False, null=False)
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    class Role(models.TextChoices):
        GUEST = 'GUEST', _('Guest')
        HOST = 'HOST', _('Host')
        ADMIN = 'ADMIN', _('Admin')
    
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def password_hash(self):  
        return self.password 


class Conversation(models.Model):
    """
    Represents a conversation between two or more users.
    """

    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    participants = models.ManyToManyField(
        User,
        related_name="conversation",
        blank=True
    )

    @override
    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Represents a single message sent within a conversation.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    message_body = models.TextField(blank=False, null=False)

    sent_at = models.DateTimeField(auto_now_add=True)

    # `sender`: A link to the User who sent the message.
    # on_delete=models.CASCADE means if the user is deleted, their messages are also deleted.
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    # **IMPORTANT ADDITION**: A message must belong to a conversation.
    # This foreign key links each message to its parent conversation.
    # This was not in the original schema but is logically required.
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    class Meta:
        # Order messages by when they were sent by default.
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at:%Y-%m-%d %H:%M}"
