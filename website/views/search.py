from django.http import HttpResponse
from django.template import loader

from website.db.fetch import get_albums_by_title, get_albums_by_cql, \
    get_codes


def searchresponse(context, request):
    template = loader.get_template('website/search.html')
    return HttpResponse(template.render(context, request))


def searchq(request, query):
    """
    search quick (search on title)
    :param request:
    :param query:
    :return:
    """
    context = {
            'query': query,
            'albums': get_albums_by_title(query)
        }
    return searchresponse(context, request)


def search(request):
    albums = get_albums_by_cql(request.GET)
    params = {
        'codes': get_codes(),
        'albums': albums,
        'mothers': albums.get('mothers'),
        'children': albums.get('children'),
    }
    return searchresponse(params, request)
