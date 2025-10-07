from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    Exposes essential fields, hides sensitive info.
    """
    # Explicit CharField usage
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.CharField()

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
    Adds sender info and validates message body.
    """
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()

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

    def validate_message_body(self, value):
        """
        Ensure message body is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model
    Includes participants and nested messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    # Explicit SerializerMethodField usage
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]
        read_only_fields = ["conversation_id", "created_at"]

    def get_messages(self, obj):
        """
        Return nested messages for this conversation.
        """
        messages = obj.message_set.all()
        return MessageSerializer(messages, many=True).data
