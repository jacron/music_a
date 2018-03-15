from django.urls import path

from website.views.album import album_delete, album_list, album, albums

urlpatterns = [
    path('<album_id>/delete/',
         album_delete),
    path('<album_id>/<list_name>/<list_id>/',
         album_list),
    path('<album_id>/',
         album,
         name='album'),
    path('',
         albums),
]
