from django.http import HttpResponse
from django.template import loader

from website.db.fetch import get_albums_ncreated


def ncreated(request, n):
    template = loader.get_template('website/ncreated.html')
    albums = get_albums_ncreated(n)
    return HttpResponse(template.render(
        {
            'items': albums
        }, request
    ))