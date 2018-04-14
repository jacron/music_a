import os
from ..db.fetch import get_componist, get_performer, get_album
from ..db.update import add_path_to_componist, add_path_to_performer
from ..lib.color import ColorPrint
from music.settings import COMPONIST_PATH, PERFORMER_PATH


def syspath_componist(componist):
    name = componist.get('LastName')
    path = None
    if name:
        path = u'{}{}'.format(COMPONIST_PATH, componist['LastName'])
    else:
        ColorPrint.print_c('{} has no last name'.format(componist),
                           ColorPrint.RED)
    return path


def create_componist_path(componist_id):
    componist = get_componist(componist_id)
    if not componist:
        ColorPrint.print_c('{} has no componist'.format(componist_id),
                           ColorPrint.RED)
        return None
    path = componist.get('Path')
    if path is None or len(path) == 0:
        path = syspath_componist(componist)
        if not os.path.exists(path):
            os.mkdir(path)
        add_path_to_componist(componist_id, componist['LastName'])
        return path
    return os.path.join(COMPONIST_PATH, path)


def syspath_performer(performer):
    name = performer['FullName']
    path = os.path.join(str(PERFORMER_PATH), name)
    return path


def create_performer_path(performer_id):
    performer = get_performer(performer_id)
    path = performer['Path']
    if path is None or len(path) == 0:
        path = syspath_performer(performer)
        if not os.path.exists(path):
            os.mkdir(path)
        add_path_to_performer(performer_id, performer['FullName'])
        return path
    return os.path.join(PERFORMER_PATH, path)


def path_from_id_field(post):
    path = None
    componist_id = post.get('componist_id')
    if componist_id:
        path = create_componist_path(componist_id)
    performer_id = post.get('performer_id')
    if performer_id:
        path = create_performer_path(performer_id)
    return path


def get_path(objectid, kind):
    if kind == 'album':
        album = get_album(objectid)
        return album['Path']
    elif kind == 'performer':
        return create_performer_path(objectid)
    elif kind == 'componist':
        return create_componist_path(objectid)
    elif kind == 'componisten':
        return COMPONIST_PATH
    return None


def decode_semi_colon(s):
    return s.replace('&semi-colon', ';')
