from django.urls import path
from website.views.librarycode import list_librarycode_instrument, \
    list_librarycode_favorite, list_librarycode, one_librarycode, \
    list_librarycoderange

urlpatterns = [
    path(
        'listrange/<code>/<crange>/<instrument_id>/',
        list_librarycoderange,
        name='librarycodelistrange'),
    path('listrange/<code>/<crange>/',
         list_librarycoderange,
         name='librarycodelistrange'),
    path('list/<code>/<instrument_id>/instrument/',
         list_librarycode_instrument,
         name='librarycodelistinstrument'),
    path('list/<code>/<favorite>/favorite/',
         list_librarycode_favorite,
         name='librarycodelistfavorite'),
    path('list/<code>/',
         list_librarycode,
         name='librarycodelist'),
    path('<librarycode>/<code>/',
         one_librarycode,
         name='librarycode'),
    path('<librarycode>/',
         one_librarycode,
         name='librarycode'),
]