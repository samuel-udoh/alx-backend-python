from email import message
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory  # Import your Message model

# The @receiver decorator connects this function to the post_save signal
@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    This function is called every time a Message instance is saved.
    """
    # The 'created' boolean is True only on the first save (i.e., object creation)
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            original_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        
        if original_message.content != instance.content:
            MessageHistory.objects.create(
                message=original_message,
                old_content = original_message.content
            )
            instance.edited = True