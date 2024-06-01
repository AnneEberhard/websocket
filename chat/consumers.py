import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Chat, Message


class ChatConsumer(WebsocketConsumer):
    """
    Manages WebSocket connections for real-time chat communication. Handles joining and leaving
    chat rooms, receiving and broadcasting messages.
    """
    def connect(self):
        """
        Handles the initial WebSocket connection.
        Joins the WebSocket to the chat room group based on the room slug.
        """
        self.room_slug = self.scope["url_route"]["kwargs"]["room_slug"]
        self.room_group_name = f"chat_{self.room_slug}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        """
        Handles the disconnection of the WebSocket.
        Removes the WebSocket from the chat room group.
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        """
        Receives a message from the WebSocket.
        Saves the message to the database if the user is authenticated and the chat room exists.
        Broadcasts the message to the room group.

        :param text_data: JSON formatted string containing the message and the room name.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        room_name = text_data_json["roomName"]
        user = self.scope["user"]

        # Save message in database
        if user.is_authenticated:
            try:
                chat = Chat.objects.get(slug=self.room_slug)  
            except Chat.DoesNotExist:
                chat = None  

            if chat:
                new_message = Message.objects.create(
                    text=message,
                    chat=chat,
                    author=user
                )
            else:
                print(f"Chat room '{room_name}' does not exist.")

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "author": user.first_name,
                "created_at": new_message.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        )

    def chat_message(self, event):
        """
        Handles messages received from the chat room group.
        Sends the message data to the WebSocket client.

        :param event: Dictionary containing message data to be sent to the WebSocket.
        """
        message = event["message"]
        author = event.get("author", "Anonymous")
        created_at = event.get("created_at", "")

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message,
            "author": author,
            "created_at": created_at
        }))
        