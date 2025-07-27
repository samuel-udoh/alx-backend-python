import  django_filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    """
    Filter for Messages.
    """
    sent_after = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    sent_before = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")

    class Meta:
        model=Message
        fields = ["sender"]

class ConversationFilter(django_filters.FilterSet):
    """
    Filter for Conversations, particularly to find a conversation with a specific user.
    """
    email = django_filters.CharFilter(
        field_name='participants__email',
        lookup_expr='iexact' # case insensitive
    )

    class Meta:
        model= Conversation
        fields = []