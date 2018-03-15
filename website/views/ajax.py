# coding=utf-8
from django.http import HttpResponse

from ..services.path import path_from_id_field
from website.views.ajaxget import do_get
from website.views.ajaxpost import do_post, path_for_person


def upload_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload(post, files):
    if post['cmd'] == 'upload':
        f = files['file']
        path = path_from_id_field(post)
        if path:
            upload_file(f, path_for_person(path).encode('UTF-8'))
            return 'Uploaded'
        return 'Not a valid componist or performer'
    pass


def ajax(request):
    msg = 'No post, files or get!'
    if request.FILES:
        msg = upload(request.POST, request.FILES)
    if request.POST:
        msg = do_post(request.POST)
    if request.GET:
        msg = do_get(request.GET)
    return HttpResponse(msg)
