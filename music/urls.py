"""music URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from website.views.ncreated import ncreated
from website.views.extra import extra, cmd_view
from website.views.home import home, ajax
from website.views.nplayed import nplayed
from website.views.pianoboek import pianoboek, pianoboeken
from website.views.image import image, imageback, image_w_h
from website.views.collection import collections, collections_search
from website.views.gather import gather
from website.views.upload import uploadalbum
from website.views.search import search, searchq
from website.urls import librarycode, componist, album, instrument, tag, \
    performer

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('hello/', include('website.urls')),
    path('album/', include(album.urlpatterns)),
    path('componist/', include(componist.urlpatterns)),
    path('librarycode/', include(librarycode.urlpatterns)),
    path('instrument/', include(instrument.urlpatterns)),
    path('tag/', include(tag.urlpatterns)),
    path('performer/', include(performer.urlpatterns)),
    path('home/', home),
    path('', search),
    path('ajax/', ajax),
    path('extra/',
         extra,
         name='extra'),
    path('extra/<cmd_code>/',
         cmd_view,
         name='cmd'),
    path('nplayed/<n>',
         nplayed,
         name='nplayed'),
    path('ncreated/<n>',
         ncreated,
         name='ncreated'),
    path('pianoboek/<id>/',
         pianoboek,
         name='pianoboek'),
    path('pianoboek/',
         pianoboeken,
         name='pianoboeken'),
    path('image/<album_id>/<image_type>/<w>/<h>',
         image_w_h,
         name='image_w_h'),
    path('image/<album_id>/<image_type>/',
         image,
         name='image'),
    path('imageback/<album_id>/<image_type>/',
         imageback,
         name='imageback'),
    path('collection/<query>/search',
         collections_search),
    path('collection/',
         collections),
    path('gather/',
         gather),
    path('gather/0/',
         gather),
    path('upload/',
         uploadalbum,
         name='upload'),
    path('search/',
         search),
    path('search/<query>',
         searchq,
         name='query'),
]
