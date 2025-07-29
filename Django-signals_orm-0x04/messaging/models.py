from tkinter import CASCADE
from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False) # New: Track read status

    class Meta:
        # New: Order messages by timestamp by default
        ordering = ['timestamp']

    def __str__(self):
        # New: A helpful string representation of the object
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp:%Y-%m-%d %H:%M}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notified_user")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notification_message")
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} about message from {self.message.sender.username}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name="history", on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    class META:
        ordering = ["-edited_at"]
    def __str__(self):
        return f"History for message {self.message.id} at {self.edited_at}"