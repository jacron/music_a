import taglib
import os

import mutagen
from tinytag import TinyTag


# from flac.db import get_album, get_pieces, get_album_performers, \
#     get_album_componisten
# from flac.services import get_extension
from website.db.fetch import get_album_performers, get_album_componisten, \
    get_album, get_pieces
from website.lib.color import ColorPrint
from website.services.services import get_extension


def performers(album_id):
    p = get_album_performers(album_id)
    return [x['FullName'] for x in p]


def composers(album_id):
    p = get_album_componisten(album_id)
    return [x['FullName'] for x in p]


def title2tag(p, title):
    song = taglib.File(p)
    try:
        song.tags['ALBUM'] = [title]
        song.save()
    except TypeError as t:
        ColorPrint.print_c(str(t), ColorPrint.CYAN)


def all2tag(p, title, album_id):
    # song = taglib.File(p)
    song = mutagen.File(p)
    try:
        song.tags['ALBUM'] = [title]
        song.tags['ARTIST'] = performers(album_id)
        song.tags['COMPOSER'] = composers(album_id)
        song.save()
    except TypeError as t:
        ColorPrint.print_c(str(t), ColorPrint.CYAN)


def set_metatags(album_id, mode):
    album = get_album(album_id)
    print(album['Title'])
    pieces = get_pieces(album_id)
    for piece in pieces:
        if get_extension(piece['Name']) != 'cue':
            p = os.path.join(album['Path'], piece['Name'])
            if mode == 'short':
                title2tag(p, album['Title'])
            if mode == 'long':
                all2tag(p, album['Title'], album['ID'])
    return ''


def get_metatags(p):
    try:
        song = mutagen.File(p)
        return song
    except Exception as ex:
        ColorPrint.print_c(str(ex), ColorPrint.CYAN)
        ColorPrint.print_c(str(p), ColorPrint.CYAN)
    return None
