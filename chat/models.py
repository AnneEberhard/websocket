from django.db import models
from datetime import date
from django.conf import settings
from django.utils import timezone


class Chat(models.Model):
    created_at = models.DateField(default=date.today)

class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateField(default=date.today)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
        # foreignkey referenziert auf ein anderes Objekt
        # on_delete=models.CASCADE sorgt dafür, dass wenn der Nutzer gelöscht wird, die Nachricht auch gelöscht wird
        # related_name='author_message_set' info für die Datenbank: es geht um author im model message
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_message_set', default=None, blank=True, null=True)
        #Standardwert ist none, wir dürfen nichts reingeben, die Datenbank akzeptiert auch nichts





