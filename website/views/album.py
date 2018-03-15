from django.http import HttpResponse
from django.template import loader

from website.db.fetch import get_albums, get_album
from website.db.update import delete_album
from website.services.album_content import album_context


def album_list(request, album_id, list_id, list_name):
    template = loader.get_template('website/album.html')
    context = album_context(album_id, list_name, list_id)
    if not context:
        return HttpResponse()
    return HttpResponse(template.render(context, request))


def album_delete(request, album_id):
    delete_album(album_id)
    template = loader.get_template('website/album_deleted.html')
    return HttpResponse(template.render({
        'album': get_album(album_id)
    }, request))


def album_view(request, album_id):
    template = loader.get_template('website/album.html')
    context = album_context(album_id)
    if not context:
        return HttpResponse()
    return HttpResponse(template.render(context, request))


def album(request, album_id):
    return album_view(request, album_id)


def albums(request):
    template = loader.get_template('website/albums.html')
    return HttpResponse(template.render(
        {'albums': get_albums(), }, request))
