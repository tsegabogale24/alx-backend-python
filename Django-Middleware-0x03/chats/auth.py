# messaging_app/chats/auth.py
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    """
    Returns refresh and access JWT tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
