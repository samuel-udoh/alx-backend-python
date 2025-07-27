from rest_framework.permissions import BasePermission
from .models import Conversation

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    This also applies to messages within that conversation.
    """
    def has_permission(self, request, view):
        """
        Global permission check for the view.
        Allows any authenticated user to access list views (like seeing all their conversations)
        or create a new conversation. Access to individual objects is handled by `has_object_permission`.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to only allow participants of a conversation to view/edit it.
        """
        # The 'obj' can be either a Conversation instance or a Message instance.
        # We need to determine the conversation from the object.
        if hasattr(obj, "conversation"):
            # This is a Message instance. Get the parent conversation.
            conversation = obj.conversation
        else:
            # This is a Conversation instance.
            conversation = obj
        return request.user and conversation.participants.all()