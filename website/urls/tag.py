from django.urls import path

from website.views.tag import tag, tag_delete, tags

urlpatterns = [
    path('<tag_id>/delete/',
        tag_delete),
    path('<tag_id>/',
        tag,
         name='tag'),
    path('',
        tags,
         name='tags'),
]
