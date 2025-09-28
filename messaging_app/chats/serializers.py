from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    Exposes essential fields, hides password & password_hash by default.
    """
    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]
        read_only_fields = ["user_id", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model
    Includes sender info and conversation reference.
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "conversation",
            "message_body",
            "sent_at",
        ]
        read_only_fields = ["message_id", "sent_at"]


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model
    Includes participants and nested messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source="message_set")

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]
        read_only_fields = ["conversation_id", "created_at"]
