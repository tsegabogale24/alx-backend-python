from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("chats.urls")),      # main app routes
    path("api-auth/", include("rest_framework.urls")),  # <-- required
]
