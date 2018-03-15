from django.http import HttpResponse
from django.template import loader

from website.db.update import delete_performer
from music import settings
from website.services.services import alfabet
from website.db.fetch import get_performers, get_performer_albums, get_performer, \
    get_performer_path

import os


def performer_delete(request, performer_id):
    performer = get_performer(performer_id)
    delete_performer(performer_id)
    template = loader.get_template('website/performer_deleted.html')
    return HttpResponse(template.render({'performer': performer}, request))


def performer(request, performer_id):
    template = loader.get_template('website/performer.html')
    context = {
        'items': get_performer_albums(performer_id),
        'performer': get_performer(performer_id)
    }
    return HttpResponse(template.render(context, request))


def has_image(performer_id):
    person_path = get_performer_path(performer_id)
    if person_path:
        try:
            image_path = os.path.join(str(person_path), settings.PERSON_FILE)
        except TypeError as t:
            print(str(t), person_path)
            return False
        return os.path.exists(image_path)
    return False


def performers(request):
    template = loader.get_template('website/performers.html')
    performers = get_performers()
    for performer in performers:
        performer['has_image'] = has_image(performer['ID'])
    context = {'performers': performers, 'letters': alfabet()}
    return HttpResponse(template.render(context, request))
