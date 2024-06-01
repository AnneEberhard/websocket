from django.urls import re_path
from . import consumers

# WebSocket URL patterns
websocket_urlpatterns = [
    # Route for chat room WebSocket connections, using the room slug to identify the room.
    # Connects incoming WebSocket requests to the ChatConsumer for handling.
    re_path(r'ws/chat/(?P<room_slug>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]
