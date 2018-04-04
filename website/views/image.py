import os

from PIL import Image
from django.http import HttpResponse, HttpResponseNotFound

from music.settings import NOT_FOUND_IMAGE_PATH
from website.db.fetch import get_album, get_componist_path, get_performer_path
from django.conf import settings


def calc(w, h, iw, ih):
    # if only width or only height is given,
    # calculate proportionally the other dimension
    if h == -1:
        wpercent = w/iw
        hsize = int(ih * float(wpercent))
        return w, hsize
    if w == -1:
        hpercent = h/ih
        wsize = int(iw * float(hpercent))
        return wsize, h
    return w, h


def redim(image_path, w, h):
    if w or h:
        thumb_path = image_path + '.thumb_' + w + '_' + h + '.png'
        if os.path.exists(thumb_path):
            # return cached file
            image_data = open(thumb_path, "rb").read()
            return HttpResponse(image_data, content_type="image/png")
        try:
            img = Image.open(image_path)
            size = calc(int(w), int(h), float(img.size[0]), float(img.size[1]))
            img.thumbnail(size, Image.ANTIALIAS)
            response = HttpResponse(content_type="image/png")
            # cache the file
            img.save(thumb_path, 'png')
            img.save(response, "png")
            return response
        except IOError:
            print("cannot create thumbnail for", image_path)
    # return the original image
    image_data = open(image_path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


def get_image(path, w=None, h=None):
    image_path = path
    if not os.path.exists(path):
        try:
            image_data = open(NOT_FOUND_IMAGE_PATH, "rb").read()
        except IOError as err:
            print(err)
            return empty_response()
        return HttpResponse(image_data, content_type="image/png")
    else:
        # image_data = open(image_path, "rb").read()
        response = redim(image_path, w, h)
        return response


def componistimage(componist_id, w=None, h=None):
    componist_path = get_componist_path(componist_id)
    if not componist_path:
        return empty_response()
    image_path = '{}/{}'.format(componist_path, settings.PERSON_FILE)
    return get_image(image_path, w, h)


def empty_response():
    return HttpResponse()


def instrumentimage(instrument_name, w=None, h=None):
    image_path = '{}{}.jpg'.format(settings.INSTRUMENTS_PATH, instrument_name)
    return get_image(image_path, w, h)


def albumimage(album_id, w=None, h=None):
    album = get_album(album_id)
    if not album:
        return HttpResponseNotFound(
            'Dit album bestaat niet:"{}"'.format(album_id), )
    if not album['Path']:
        return empty_response()
    image_path = album['Path'] + settings.COVER_FILE
    return get_image(image_path, w, h)


def albumimageback(album_id):
    album = get_album(album_id)
    if not album:
        return HttpResponseNotFound(
            'Dit album bestaat niet:"{}"'.format(album_id), )
    if not album['Path']:
        return empty_response()
    image_path = album['Path'] + settings.BACK_FILE
    return get_image(image_path)


def performerimage(performer_id, w=None, h=None):
    performer_path = get_performer_path(performer_id)
    if not performer_path:
        return empty_response()
    image_path = os.path.join(str(performer_path), settings.PERSON_FILE)
    return get_image(image_path, w, h)


def librarycodeimage(k_code, w=None, h=None):
    image_path = settings.LIBRARYCODE_PATH + k_code + '.png'
    return get_image(image_path, w, h)


def imageback(request, album_id, image_type):
    if image_type == 'album':
        return albumimageback(album_id)


def image_w_h(request, album_id, image_type, w, h):
    if image_type == 'album':
        return albumimage(album_id, w, h)
    if image_type == 'performer':
        return performerimage(album_id, w, h)
    if image_type == 'componist':
        return componistimage(album_id, w, h)
    if image_type == 'instrument':
        return instrumentimage(album_id, w, h)
    if image_type == 'librarycode':
        return librarycodeimage(album_id, w, h)
    return HttpResponse('unknown image_type:' + image_type)


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
