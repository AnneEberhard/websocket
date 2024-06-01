import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Chat, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        room_name = text_data_json["roomName"]
        user = self.scope["user"]

        # Save message in database
        if user.is_authenticated:
            try:
                chat = Chat.objects.get(room_name=room_name)  
            except Chat.DoesNotExist:
                chat = None  # Optional: Erstelle den Chatraum, wenn er nicht existiert

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

    # Receive message from room group
    def chat_message(self, event):
        print("Broadcasting message:", event)
        message = event["message"]
        author = event.get("author", "Anonymous")
        created_at = event.get("created_at", "")

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message,
            "author": author,
            "created_at": created_at
        }))