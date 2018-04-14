import glob

from PIL import ImageGrab

from website.db.fetch import get_album
from website.lib.color import ColorPrint

from website.services.path import create_componist_path, create_performer_path
from music.settings import COVER_PATH, TMP_PATH, SCORE_FRAGMENT_PATH, \
    PERSON_FILE, COVER_FILE
import os

from website.services.services import openpath

rug = 0


def save_score_fragment():
    # img = ImageGrab.grabclipboard()
    # if img:
    #     img.save(SCORE_FRAGMENT_PATH.format(code))
    pass


def delete_score_fragment(code):
    img_path = SCORE_FRAGMENT_PATH.format(code)
    os.remove(img_path)


def get_person_image_path(person_id, ptype):
    image_path = None
    if ptype == 'componist':
        image_path = create_componist_path(person_id)
    if ptype == 'performer':
        image_path = create_performer_path(person_id)
    return image_path


def clipboard_save(path, file):
    img = ImageGrab.grabclipboard()
    if img:
        img.save(os.path.join(path, file))
        ColorPrint.print_c(file + ' saved!', ColorPrint.LIGHTCYAN)
    else:
        ColorPrint.print_c('No image on clipboard!', ColorPrint.RED)


def clipboard_save_path(path):
    img = ImageGrab.grabclipboard()
    if img:
        img.save(path)
        ColorPrint.print_c(path + ' saved!', ColorPrint.LIGHTCYAN)
    else:
        ColorPrint.print_c('No image on clipboard!', ColorPrint.RED)


def save_person_remote(person_id, ptype):
    image_path = get_person_image_path(person_id, ptype)
    if image_path:
        clipboard_save(image_path, PERSON_FILE)
        return True
    return False


def remove_cached_cover(album_path):
    p = os.path.join(album_path, 'folder*.png')
    for f in glob.iglob(p):
        # print(f)
        os.remove(f)


def save_album(album_id):
    album = get_album(album_id)
    image_path = album['Path'] + COVER_FILE
    if os.path.exists(image_path):
        os.remove(image_path)
    #     todo: remove all cached folder files
        remove_cached_cover(album['Path'])
    try:
        clipboard_save_path(album['Path'] + COVER_FILE)
    except PermissionError as pe:
        print(str(pe))
        print(image_path)
        return 'not saved'
    except FileNotFoundError as fe:
        print(str(fe))
        print(image_path)
        return 'not saved'
    return 'saved from clipboard:' + image_path


def save_person(person_id, ptype):
    # save_person_grab(id, type)
    if save_person_remote(person_id, ptype):
        return 'image saved from clipboard for person {}, type {}'\
            .format(person_id, ptype)
    return 'image not saved'


def crop_front(img):
    width = img.size[0]
    height = img.size[1]
    fbox = (width / 2 + rug, 0, width, height)
    return img.crop(fbox)


def crop_back(img):
    width = img.size[0]
    height = img.size[1]
    bbox = (0, 0, width / 2 - rug, height)
    return img.crop(bbox)


def save_cb_images(cover, nback):
    img = ImageGrab.grabclipboard()
    if img:
        front = crop_front(img)
        back = crop_back(img)
        front.save(COVER_PATH.format(cover))
        back.save(COVER_PATH.format(nback))
        openpath(TMP_PATH)
    else:
        ColorPrint.print_c('no valid image on clipboard', ColorPrint.RED)


def save_cb_image(cover):
    img = ImageGrab.grabclipboard()
    if img:
        img.save(COVER_PATH.format(cover))
        openpath(TMP_PATH)
    else:
        ColorPrint.print_c('no valid image on clipboard', ColorPrint.RED)
