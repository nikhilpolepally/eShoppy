"""
WSGI config for eShoppy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from wsgiref.util import application_uri

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eShoppy.settings')
application = get_wsgi_application()
application = WhiteNoise(application, root="/static")
application.add_files("/static", prefix="more-files/")
