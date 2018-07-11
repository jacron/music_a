"""
WSGI config for music project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/Users/orion/PycharmProjects/music_a/music')


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music.settings")

application = get_wsgi_application()
# def application(environ, start_response):
#     if environ['mod_wsgi.process_group'] != '':
#         import signal
#         os.kill(os.getpid(), signal.SIGINT)
#     return ["killed"]