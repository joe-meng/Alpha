"""
WSGI config for alpha project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alpha.settings.defaults")
print((' Init Django with: %s ' % os.environ.get('DJANGO_SETTINGS_MODULE')).center(80, '-'))

application = get_wsgi_application()

