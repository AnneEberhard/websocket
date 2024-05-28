"""
WSGI config for django_chat_app project.

WSGI is the Web Server Gateway Interface.
It is a specidfication that describes how a web server communicates with web applications,
and how web applications can be chained rogether to process one requests.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chat_app.settings')

application = get_wsgi_application()
