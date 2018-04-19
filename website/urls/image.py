from django.urls import path

from website.views.image import image_w_h, imageback_w_h, imageback, image, \
    imagebr

urlpatterns = [
    path('<album_id>/<image_type>/<w>/<h>',
         image_w_h,
         name='image_w_h'),
    path('<album_id>/<image_type>/',
         image,
         name='image'),
    path('back/<album_id>/<image_type>/<w>/<h>',
         imageback_w_h,
         name='imageback_w_h'),
    path('back/<album_id>/<image_type>/',
         imageback,
         name='imageback'),
    path('br/',
         imagebr,
         name='imagebr'),
]