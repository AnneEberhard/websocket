from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify


class Chat(models.Model):
    room_name = models.CharField(max_length=255, unique=True, default='')
    slug = models.SlugField(max_length=255, unique=True, blank=True,default='')
    created_at = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.room_name)
        super(Chat, self).save(*args, **kwargs)    


class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set', default=None, blank=True, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_message_set', default=None, blank=True, null=True)
        