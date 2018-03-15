from django.urls import path
from website.views.componist import componist, componist_delete, componist_search, \
    componisten_period, componisten

urlpatterns = [
    path('<componist_id>/delete/',
         componist_delete),
    path('<period>/period/',
         componisten_period),
    path('<componist_id>/search/<query>/',
        componist_search),
    path('<componist_id>/',
         componist,
         name='componist'),
    path('',
         componisten,
         name='componisten'),
]