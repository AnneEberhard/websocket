from django.contrib import admin
from .models import Chat, Message

class MessageAdmin(admin.ModelAdmin):
    # Defines the fields that should appear in the forms in the admin interface.
    fields = ('chat', 'text', 'created_at', 'author', 'receiver')

    # Customizes which columns should appear in the list display of messages.
    list_display = ('created_at', 'author', 'text', 'chat')

    # Enables search functionality in the admin list display based on the message text.
    search_fields = ('text',)

# Register the Message model with the customized admin interface.
admin.site.register(Message, MessageAdmin)

# Register the Chat model with the default admin interface.
admin.site.register(Chat)

