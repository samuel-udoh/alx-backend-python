# In your_app_name/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification  # Import your Message model

# The @receiver decorator connects this function to the post_save signal
@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    This function is called every time a Message instance is saved.
    """
    # The 'created' boolean is True only on the first save (i.e., object creation)
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)