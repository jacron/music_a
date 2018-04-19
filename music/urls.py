"""music path Configuration

"""
from django.contrib import admin
from django.urls import path, include

from website.views.ncreated import ncreated
from website.views.extra import extra, cmd_view
from website.views.home import home, ajax
from website.views.nplayed import nplayed
from website.views.pianoboek import pianoboek, pianoboeken
from website.views.image import image, imageback, image_w_h, imageback_w_h
from website.views.collection import collections, collections_search
from website.views.gather import gather
from website.views.upload import uploadalbum
from website.views.search import search, searchq
from website.urls import librarycode, componist, album, instrument, tag, \
    performer, image

urlpatterns = [
    # path('admin/', admin.site.paths),
    path('album/', include(album.urlpatterns)),
    path('componist/', include(componist.urlpatterns)),
    path('librarycode/', include(librarycode.urlpatterns)),
    path('instrument/', include(instrument.urlpatterns)),
    path('tag/', include(tag.urlpatterns)),
    path('performer/', include(performer.urlpatterns)),
    path('image/', include(image.urlpatterns)),
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
