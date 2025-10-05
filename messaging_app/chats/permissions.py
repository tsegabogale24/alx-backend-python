from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own objects.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API
    - Only participants of a conversation can send, view, update, or delete messages
    """
    def has_permission(self, request, view):
        # Only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Assumes:
        - Message model has a ForeignKey to Conversation (obj.conversation)
        - Conversation model has participants ManyToMany field
        """

        # Check participant first
        if request.user not in obj.conversation.participants.all():
            return False

        # Allow participants to view messages (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow only message owner to update or delete
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.user == request.user

        # Allow sending new messages (POST) if participant
        if request.method == "POST":
            return True

        return False
