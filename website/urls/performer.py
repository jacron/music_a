from django.urls import path

from website.views.performer import performer, performer_delete, performers

urlpatterns = [
    path('<performer_id>/delete/',
         performer_delete),
    path('<performer_id>/',
         performer,
         name='performer'),
    path('',
         performers,
         name='performers'),
]
