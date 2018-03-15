from django.http import HttpResponse
from django.template import loader

from website.db.fetch import get_pieces_nplayed


def nplayed(request, n):
    template = loader.get_template('website/nplayed.html')
    pieces = get_pieces_nplayed(n)
    return HttpResponse(template.render(
        {
            'items': pieces
        }, request
    ))