from rest_framework import viewsets
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from .filters import MessageFilter, ConversationFilter
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.exceptions import PermissionDenied
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filterset_class = ConversationFilter

    def get_queryset(self):
        """
        This view should only return a list of all the conversations
        for the currently authenticated user.
        """
        user = self.request.user
        conversation = get_object_or_404(Conversation, pk=self.kwargs['conversation_pk'])

        if user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant of this conversation.", code=HTTP_403_FORBIDDEN)
        return Conversation.objects.filter(participants=user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filterset_class = MessageFilter
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']  # newest message first

    def get_queryset(self):
        """
        This view should only return messages for the conversation
        specified in the URL.
        """
        conversation_pk = self.kwargs['conversation_pk']
        return Message.objects.filter(conversation_id=conversation_pk)

    def perform_create(self, serializer):
        """
        The simplest way to fix the error.
        This automatically sets the conversation on the message
        using the ID from the URL.
        """
        # 1. Get the conversation object from the database using the ID from the URL.
        conversation = get_object_or_404(Conversation, pk=self.kwargs['conversation_pk'])
    
        sender = self.request.user

        # 2. Save the message, manually adding the conversation object.
        serializer.save(conversation=conversation, sender=sender)