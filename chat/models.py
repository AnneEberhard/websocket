from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify


class Chat(models.Model):
    """
    Represents a chat room where users can exchange messages.

    Attributes:
        room_name (str): The name of the chat room.
        slug (str): URL-friendly version of the chat room name, used in links and routing.
        created_at (date): The date when the chat room was created.
    """
    room_name = models.CharField(max_length=255, unique=True, default='')
    slug = models.SlugField(max_length=255, unique=True, blank=True, default='')
    created_at = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        Overridden save method to automatically generate a slug from the room name.
        """
        self.slug = slugify(self.room_name)
        super(Chat, self).save(*args, **kwargs)


class Message(models.Model):
    """
    Represents a message sent by a user in a chat room.

    Attributes:
        text (str): The text content of the message.
        created_at (date): The date and time the message was created.
        author (User): The user who authored the message. Related to AUTH_USER_MODEL.
        receiver (User): The user who is the intended recipient of the message, if any.
                         Optional, can be null if the message is for the entire room.
        chat (Chat): The chat room in which this message was posted.
    """
    text = models.CharField(max_length=500)
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set', default=None, blank=True, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_message_set', default=None, blank=True, null=True)
