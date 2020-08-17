"""
WSGI config for api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import logging
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
from django.conf import settings

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO, format='(asctime)s %(name)-12s %(levelname)-8s %(message)s')

application = get_wsgi_application()
