from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from website.db.fetch import get_instrument, get_instrument_albums, get_instruments, \
    get_instrument_albums_search
from website.db.update import delete_instrument


def instrument_delete(request, instrument_id):
    instrument = get_instrument(instrument_id)
    delete_instrument(instrument_id)
    template = loader.get_template('website/instrument_deleted.html')
    return HttpResponse(template.render({
        'instrument': instrument,
    }, request))


def instrument_search(request, instrument_id, query):
    template = loader.get_template('website/instrument.html')
    context = {
        'items': get_instrument_albums_search(instrument_id, query),
        'instrument': get_instrument(instrument_id),
        'instruments_path': settings.INSTRUMENTS_PATH,
        'instrument_id': instrument_id,
        'query': query,
    }
    return HttpResponse(template.render(context, request))


def instrument(request, instrument_id):
    template = loader.get_template('website/instrument.html')
    context = {
        'items': get_instrument_albums(instrument_id),
        'instrument': get_instrument(instrument_id),
        'instruments_path': settings.INSTRUMENTS_PATH,
        'instrument_id': instrument_id,
    }
    return HttpResponse(template.render(context, request))


def instrumenten(request):
    context = {
        'items': get_instruments(),
        'instruments_path': settings.INSTRUMENTS_PATH
    }
    template = loader.get_template('website/instrumenten.html')
    return HttpResponse(template.render(context, request))
