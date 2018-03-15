# import sys, os, django
# from django.core.wsgi import get_wsgi_application
#
# proj_path = '/Users/orion/PycharmProjects/music/music'
# # sys.path.append(proj_path)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music.settings')
# os.chdir(proj_path)
# application = get_wsgi_application()

# django.setup()

# export PATH=$PATH:/Users/orion/PycharmProjects/music/music

import music.wsgi
