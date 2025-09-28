from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversations.
    Supports listing, retrieving, creating conversations,
    and retrieving messages within a conversation.
    """
    queryset = Conversation.objects.all().order_by("-created_at")
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expected payload:
        {
            "participants": [user_id1, user_id2, ...]
        }
        """
        participants = request.data.get("participants")
        if not participants:
            return Response(
                {"error": "At least one participant is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        """
        Custom action: get messages for a conversation.
        """
        conversation = self.get_object()
        messages = conversation.messages.all().order_by("sent_at")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Messages.
    Supports listing and creating messages inside conversations.
    """
    queryset = Message.objects.all().order_by("-sent_at")
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Expected payload:
        {
            "conversation": "<conversation_id>",
            "sender": "<user_id>",
            "message_body": "Hello!"
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = serializer.validated_data["conversation"].conversation_id
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        message = Message.objects.create(
            conversation=conversation,
            sender=serializer.validated_data["sender"],
            message_body=serializer.validated_data["message_body"],
        )
        output_serializer = self.get_serializer(message)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
