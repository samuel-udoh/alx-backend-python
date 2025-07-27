from rest_framework import serializers
from .models import User, Conversation, Message
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ["first_name", "last_name", "email", "phone_number", "role"]

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    conversation  = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Message
        fields=["message_id", "message_body", "sent_at", "sender", "conversation"]

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields=["conversation_id", "created_at", "participants", "messages"]
