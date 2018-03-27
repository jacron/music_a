import os
from django.http import HttpResponse, HttpResponseNotFound

from music.settings import NOT_FOUND_IMAGE_PATH
from website.db.fetch import get_album, get_componist_path, get_performer_path
from django.conf import settings


def get_image(path):
    image_path = path
    try:
        image_data = open(image_path, "rb").read()
    except IOError:
        try:
            image_data = open(NOT_FOUND_IMAGE_PATH, "rb").read()
        except IOError as err:
            print(err)
            return empty_response()
    return HttpResponse(image_data, content_type="image/png")


def componistimage(componist_id):
    componist_path = get_componist_path(componist_id)
    if not componist_path:
        return empty_response()
    image_path = '{}/{}'.format(componist_path, settings.PERSON_FILE)
    return get_image(image_path)


def empty_response():
    return HttpResponse()


def instrumentimage(instrument_name):
    image_path = '{}{}.jpg'.format(settings.INSTRUMENTS_PATH, instrument_name)
    return get_image(image_path)


def albumimage(album_id):
    album = get_album(album_id)
    if not album:
        return HttpResponseNotFound(
            'Dit album bestaat niet:"{}"'.format(album_id), )
    if not album['Path']:
        return empty_response()
    image_path = album['Path'] + settings.COVER_FILE
    return get_image(image_path)


def albumimageback(album_id):
    album = get_album(album_id)
    if not album:
        return HttpResponseNotFound(
            'Dit album bestaat niet:"{}"'.format(album_id), )
    if not album['Path']:
        return empty_response()
    image_path = album['Path'] + settings.BACK_FILE
    return get_image(image_path)


def performerimage(performer_id):
    performer_path = get_performer_path(performer_id)
    if not performer_path:
        return empty_response()
    image_path = os.path.join(str(performer_path), settings.PERSON_FILE)
    return get_image(image_path)


def librarycodeimage(k_code):
    image_path = settings.LIBRARYCODE_PATH + k_code + '.png'
    return get_image(image_path)


def imageback(request, album_id, image_type):
    if image_type == 'album':
        return albumimageback(album_id)


def image(request, album_id, image_type):
    if image_type == 'album':
        return albumimage(album_id)
    if image_type == 'performer':
        return performerimage(album_id)
    if image_type == 'componist':
        return componistimage(album_id)
    if image_type == 'instrument':
        return instrumentimage(album_id)
    if image_type == 'librarycode':
        return librarycodeimage(album_id)
    return HttpResponse('unknown image_type:' + image_type)
