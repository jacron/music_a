import os
import mutagen
from mutagen import MutagenError
from mutagen.apev2 import APEBadItemError

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
    song = mutagen.File(p)
    try:
        song.tags['ALBUM'] = [title]
        song.save()
    except TypeError as t:
        ColorPrint.print_c(str(t), ColorPrint.CYAN)


def all2tag(p, title, album_id):
    song = mutagen.File(p)
    try:
        song.tags['ALBUM'] = [title]
        song.tags['ARTIST'] = performers(album_id)
        song.tags['COMPOSER'] = composers(album_id)
        song.save()
    except TypeError as t:
        ColorPrint.print_c(str(t), ColorPrint.CYAN)


def remove_tag(p, tag):
    song = mutagen.File(p)
    try:
        del song[tag]
        song.save()
    except TypeError as te:
        ColorPrint.print_c(str(te), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)
    except MutagenError as t:
        ColorPrint.print_c(str(t), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)
    except APEBadItemError as a:
        ColorPrint.print_c(str(a), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)


def remove_taggeneric(album_id, tag):
    album = get_album(album_id)
    print(album['Title'])
    pieces = get_pieces(album_id)
    for piece in pieces:
        if get_extension(piece['Name']) != 'cue':
            p = os.path.join(album['Path'], piece['Name'])
            remove_tag(p, tag)
    return ''


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
    except MutagenError as t:
        ColorPrint.print_c(str(t), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)
    except Exception as ex:
        ColorPrint.print_c(str(ex), ColorPrint.CYAN)
        ColorPrint.print_c(str(p), ColorPrint.CYAN)
    return None
