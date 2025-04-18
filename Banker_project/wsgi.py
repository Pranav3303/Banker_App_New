"""
WSGI config for Banker_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Banker_project.settings')

application = get_wsgi_application()

app = application

app = WhiteNoise(
    application,
    root=os.path.join(os.path.BASE_DIR,"own_repo"),
    prefix="static/"
)

application.add_files(
    os.path.join(os.path.BASE_DIR,"gallery"),
    prefix="gallery/"
)