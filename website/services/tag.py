import os
# import mutagen
from mutagen import MutagenError, id3
from mutagen.apev2 import APEBadItemError
from mutagen.flac import Picture

from music.settings import INTERESTING_METATAGS
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
    import mutagen
    song = mutagen.File(p)
    try:
        song.tags['ALBUM'] = [title]
        song.save()
    except TypeError as t:
        ColorPrint.print_c(str(t), ColorPrint.CYAN)


def get_album_metatags(album_path, pieces):
    album_metatags = {}
    if len(pieces):
        path = u'{}/{}'.format(album_path, pieces[0]['Name'])
        metatags = get_metatags(path)
        if metatags:
            for tag in INTERESTING_METATAGS:
                if metatags.get(tag):
                    album_metatags[tag] = metatags[tag]
    return album_metatags


def all2tag(p, title, album_id):
    import mutagen
    song = mutagen.File(p)
    try:
        song.tags['ALBUM'] = [title]
        song.tags['ARTIST'] = performers(album_id)
        song.tags['COMPOSER'] = composers(album_id)
        song.save()
    except TypeError as t:
        ColorPrint.print_c(str(t), ColorPrint.CYAN)


def set_pic(p, pic):
    import mutagen
    song = mutagen.File(p)
    # try:
    song.add_picture(pic)
    song.save()
    # except


def set_tag(p, tag, value):
    import mutagen
    song = mutagen.File(p)
    try:
        song[tag] = value
        song.save()
    except KeyError as ke:
        ColorPrint.print_c('key not found: ' + str(ke), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)
    except TypeError as te:
        ColorPrint.print_c('type error: ' + str(te), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)
    except MutagenError as t:
        ColorPrint.print_c(str(t), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)
    except APEBadItemError as a:
        ColorPrint.print_c(str(a), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)


def delete_tag(p, tag):
    import mutagen
    song = mutagen.File(p)
    try:
        del song[tag]
        song.save()
    except KeyError as ke:
        ColorPrint.print_c('key not found: ' + str(ke), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)
    except TypeError as te:
        ColorPrint.print_c('type error: ' + str(te), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)
    except MutagenError as t:
        ColorPrint.print_c(str(t), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)
    except APEBadItemError as a:
        ColorPrint.print_c(str(a), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)


def remove_tag(album_id, tag):
    album = get_album(album_id)
    print(album['Title'])
    pieces = get_pieces(album_id)
    for piece in pieces:
        if get_extension(piece['Name']) != 'cue':
            p = os.path.join(album['Path'], piece['Name'])
            delete_tag(p, tag)
    return ''


def tag_get_piece_paths(album_id):
    album = get_album(album_id)
    print(album['Title'])
    pieces = get_pieces(album_id)
    paths = []
    for piece in pieces:
        if get_extension(piece['Name']) != 'cue':
            paths.append(os.path.join(album['Path'], piece['Name']))
    return paths


def set_metatags(album_id, mode):
    album = get_album(album_id)
    for p in tag_get_piece_paths(album_id):
        if mode == 'short':
            title2tag(p, album['Title'])
        if mode == 'long':
            all2tag(p, album['Title'], album['ID'])
    return ''


def get_metatags(p):
    try:
        import mutagen
        return mutagen.File(p)
        # ntags = {}
        # for tag, value in tags.tags:
        #     if tag != 'cuesheet' and tag !='APIC:':
        #         ntags[tag] = value
        # return ntags
    except MutagenError as t:
        ColorPrint.print_c(str(t), ColorPrint.CYAN)
        ColorPrint.print_c(p, ColorPrint.BLUE)
    except Exception as ex:
        ColorPrint.print_c(str(ex), ColorPrint.CYAN)
        ColorPrint.print_c(str(p), ColorPrint.CYAN)
    return None


def tag_set_metatag(tag, value, album_id):
    values = value.split('/')
    for p in tag_get_piece_paths(album_id):
        set_tag(p, tag, values)
    return ''


def tag_remove_metatag(tag, album_id):
    for p in tag_get_piece_paths(album_id):
        delete_tag(p, tag)
    return ''


def tag_put_picture(album_id):
    pic = Picture()
    album = get_album(album_id)
    with open(album['Path'] + "/folder.jpg", "rb") as f:
        pic.data = f.read()
    if not pic.data:
        return 'No folder.jpg found'
    pic.type = id3.PictureType.COVER_FRONT
    pic.mime = u"image/jpeg"
    pic.width = 500
    pic.height = 500
    pic.depth = 16
    for p in tag_get_piece_paths(album_id):
        set_pic(p, pic)
    return 'success'
