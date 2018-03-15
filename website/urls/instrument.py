from django.urls import path

from website.views.instrument import instrument, instrumenten, instrument_delete, \
    instrument_search

urlpatterns = [
    path('<instrument_id>/delete/<query>/',
         instrument_delete),
    path('<instrument_id>/search/<query>/',
         instrument_search),
    path('<instrument_id>/',
         instrument),
    path('',
         instrumenten),
]
