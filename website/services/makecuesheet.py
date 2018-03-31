import codecs
import glob
import os

from music.settings import MUSIC_FILES
from ..db.connect import connect
from ..db.fetch import get_album_path_by_id, get_piece, \
    get_pieces, get_album
from ..db.insert import insert_piece
from ..lib.color import ColorPrint
from ..scripts.splitflac import split_flac
from ..services.cuesheet import get_full_cuesheet
from ..services.services import subl_path, filename, trimextension, \
    get_extension, get_filename


'''
    todo: Uit het oorspronkelijke cuesheet worden niet alle, maar wel de meeste gegevens
    overgenomen, bijvoorbeeld performer en rem regels wel maar een extra index 00
    bij een track niet.
    
'''
def write_cuesheet(name, album_id, lines):
    content = ''
    for line in lines:
        content += line + '\n'
    conn, cursor = connect()
    cuename = '{}.cue'.format(name)
    path = get_album_path_by_id(album_id, cursor)
    wpath = '{}/{}'.format(path, cuename)
    # https://stackoverflow.com/questions/934160/write-to-utf-8-file-in-python
    with codecs.open(wpath, 'w', 'utf-8') as f:
        f.write('\ufeff')
        f.write('{}'.format(content))
    insert_piece(
        name=cuename,
        code=0,
        album_id=album_id,
        c=cursor,
        conn=conn)


def get_cuesheets_of_album(album_id, c):
    """
    returns cuesheets (Name, ID)
    :param album_id: int
    :param c:
    :return:
    """
    pieces = get_pieces(album_id)  # Name, ID, LibraryCode
    cuesheets = []
    other = []
    for item in pieces:
        ext = get_extension(item['Name'])
        if ext == 'cue':
            cuesheets.append(item)
        else:
            other.append(item)
    return cuesheets, other


def split_one_cue_album(album_id):
    conn, cursor = connect()
    path = get_album_path_by_id(album_id, cursor)
    cuesheets, other = get_cuesheets_of_album(album_id, cursor)
    cue = cuesheets[0]
    src = '{}/{}'.format(path, cue['Name'])
    split_flac(src, album_id)
    return src


def split_cue_album(album_id):
    """
    split album by using cuesheets that match their names
    with names of pieces (.ape)
    :param album_id:
    :return:
    """
    conn, cursor = connect()
    path = get_album_path_by_id(album_id, cursor)
    cuesheets, other = get_cuesheets_of_album(album_id, cursor)
    for cuesheet in sorted(cuesheets, key=lambda cuesheet: cuesheet['Name']):
        for o in other:
            if get_filename(cuesheet['Name']) == get_filename(o['Name']):
                src = '{}/{}'.format(path, cuesheet['Name'])
                print(src)
                split_flac(src, album_id)
    return ''


def split_cued_file(piece_id, album_id):
    # ColorPrint.print_c(piece_id, album_id)
    conn, cursor = connect()
    path = get_album_path_by_id(album_id, cursor)
    piece = get_piece(piece_id)
    src = '{}/{}'.format(path, piece['Name'])
    split_flac(src, album_id)
    return src


def cuesheet_title_from_filename(piece_id, album_id):
    conn, cursor = connect()
    path = get_album_path_by_id(album_id, cursor)
    piece = get_piece(piece_id)
    # cuesheet = get_full_cuesheet(path, piece_id)
    return trimextension(piece['Name'])


def edit_cuesheet(piece_id, album_id):
    conn, cursor = connect()
    path = get_album_path_by_id(album_id, cursor)
    if not path:
        return 'path not found for album ID=' + album_id
    piece = get_piece(piece_id)
    src = '{}/{}'.format(path, piece['Name'])
    return subl_path(src)


# def rename_cuesheet(piece_id, album_id):
#     print(piece_id, album_id)
#     conn, cursor = connect()
#     path = get_album_path_by_id(album_id, cursor)
#     piece = get_piece(piece_id)
#     src = '{}/{}'.format(path, piece['Name'])
#     if os.path.exists(src):
#         # change extension from 'cue' to 'cuex'
#         trg = '{}x'.format(src)
#         if not os.path.exists(trg):
#             os.rename(src, trg)
#             print('renamed to:{}'.format(trg))
#             return 'cuesheet extension renamed'
#         return 'renamed file already exists'
#     return 'file not found'


def rename_cuesheet(piece_id, album_id, newname):
    conn, cursor = connect()
    path = get_album_path_by_id(album_id, cursor)
    piece = get_piece(piece_id)
    src = '{}/{}'.format(path, piece['Name'])
    dst = '{}/{}.cue'.format(path, newname)
    os.rename(src, dst)


def make_cuesheet(name, ids, album_id):
    lines = []
    lines.append('TITLE "{}"'.format(filename(name)))
    # titles = []
    # print(ids)
    if len(ids) < 2:
        ColorPrint.print_c(name + ' :less than 2 ids, so quitting',
                           ColorPrint.RED)
        return
    for piece_id in ids:
        piece = get_piece(piece_id)
        fpath = piece.get('Name')
        title = trimextension(filename(fpath))
        # titles.append(title)
        lines.append('FILE "{}" WAVE'.format(fpath))
        lines.append('  TRACK 01 AUDIO')
        lines.append('    TITLE "{}"'.format(title))
        lines.append('    INDEX 01 00:00:00')
    write_cuesheet(name, album_id, lines)


def get_dirs(path):
    dirs = []
    for d in os.listdir(path):
        if os.path.isdir(os.path.join(path, d)):
            dirs.append(d)
    return sorted(dirs)


def make_sub_cuesheet(path):
    """
    Create lines for a new cuesheet
    :param path:
    :return:
    """
    lines = []
    for card in MUSIC_FILES:
        if card == 'cue':
            continue
        files_path = "{}{}".format(path, "/*.{}".format(card))
        for f in sorted(glob.iglob(files_path)):
            print(f)
            parts = f.split('/')[-2:]
            fname = '/'.join(parts)  # include subdir in fname
            title = trimextension(filename(f))
            lines.append('TITLE "{}"'.format(title))
            lines.append('FILE "{}" WAVE'.format(fname))
            lines.append('  TRACK 01 AUDIO')
            lines.append('    TITLE "{}"'.format(title))
            lines.append('    INDEX 01 00:00:00')
    return lines


def make_subs_cuesheet(album_id):
    """
    For each subdirectory, create cuesheet for pieces
    :param album_id:
    :return:
    """
    conn, c = connect()
    path = get_album_path_by_id(album_id, c)
    dirs = get_dirs(path)
    for d in dirs:
        p = os.path.join(path, d)
        lines = make_sub_cuesheet(p)
        if len(lines):
            write_cuesheet(filename(p), album_id, lines)


def remove_cuesheet(piece_id, album_id):
    conn, cursor = connect()
    path = get_album_path_by_id(album_id, cursor)
    piece = get_piece(piece_id)
    path = '{}/{}'.format(path, piece['Name'])
    os.remove(path)


def norm_cuesheet(piece_id, album_id):
    conn, cursor = connect()
    path = get_album_path_by_id(album_id, cursor)
    piece = get_piece(piece_id)
    src = '{}/{}'.format(path, piece['Name'])
    cuesheet = get_full_cuesheet(src, album_id)
    lines = []
    lines.append('TITLE "{}"'.format(cuesheet['Title']))
    cue = cuesheet['cue']
    for rem in cue['rem']:
        lines.append('REM {}'.format(rem))
    if cue['performer']:
        lines.append(('PERFORMER {}'.format(cue['performer'])))
    for cfile in cue['files']:
        fpath = os.path.join(path, cfile['name'])
        lines.append('FILE "{}" WAVE'.format(fpath))
        stored_title = None
        for track in cfile['tracks']:
            track_title = track['title']
            if stored_title and track_title[0] == '-':
                track_title = stored_title + track_title
            else:
                parts = track_title.split('-')
                stored_title = parts[0]
            lines.append('  TRACK {} AUDIO'.format(track['nr']))
            lines.append('    TITLE "{}"'.format(track_title))
            if track['performer']:
                lines.append(('    PERFORMER {}'.format(track['performer'])))
            lines.append('    INDEX {} {}'.format(
                track['index']['nr'], track['index']['time']))
    content = ''
    for line in lines:
        content += line + '\n'
    trg = os.path.dirname(src) + '/norm_' + filename(src)
    with codecs.open(trg, 'w', 'utf-8') as f:
        f.write('\ufeff')
        f.write('{}'.format(content))


def read_cuesheets(p, album_id):
    lines = []
    files_path = "{}{}".format(p, "/*.cue")
    for f in glob.iglob(files_path):
        parts = f.split('/')[-2:]
        dirname = parts[0]
        cuesheet = get_full_cuesheet(f, album_id)
        cue = cuesheet['cue']
        for rem in cue['rem']:
            lines.append('REM {}'.format(rem))
        if cue['performer']:
            lines.append(('PERFORMER {}'.format(cue['performer'])))
        for cfile in cue['files']:
            fpath = '{}/{}'.format(dirname, cfile['name'])
            lines.append('FILE "{}" WAVE'.format(fpath))
            for track in cfile['tracks']:
                lines.append('  TRACK {} AUDIO'.format(track['nr']))
                if track.get('title'):
                    title = track['title']
                    try:
                        line = '    TITLE "{}"'.format(title)
                    except:
                        line = '    TITLE "track {}"'.format(track['nr'])
                else:
                    line = '    TITLE "track {}"'.format(track['nr'])
                lines.append(line)
                if track.get('performer'):
                    lines.append('    PERFORMER {}'
                                 .format(track['performer']))
                lines.append('    INDEX {} {}'.format(
                    track['index']['nr'], track['index']['time']))
    return lines


def write_full_cuesheet(wpath, cuesheet):
    cue = cuesheet['cue']
    with codecs.open(wpath, 'w', 'utf-8') as f:
        f.write('\ufeff')
        f.write('TITLE "{}"\n'.format(cue['title']))
        f.write('PERFORMER "{}"\n'.format(cue['performer']))
        for rem in cue['rem']:
            f.write('REM {}\n'.format(rem))
        for ff in cue['files']:
            f.write('FILE "{}" WAVE\n'.format(ff['name']))
            for t in ff['tracks']:
                f.write('  TRACK {} {}\n'.format(t['nr'], t['name']))
                f.write('    TITLE "{}"\n'.format(t['title']))
                f.write('    INDEX {} {}\n'.format(t['index']['nr'],
                                                 t['index']['time']))


def combine_sub_cuesheets(album_id):
    """
    Combine cuesheets in each subdirectory in one,
    which you write in the directory

    :param album_id:
    :return:
    """
    conn, c = connect()
    path = get_album_path_by_id(album_id, c)
    dirs = sorted(get_dirs(path))
    lines = []
    title = 'combined'
    lines.append('TITLE "{}"'.format(title))
    for d in dirs:
        p = os.path.join(path, d)
        lines += read_cuesheets(p, album_id)
    if len(lines):
        write_cuesheet(title, album_id, lines)


def cuesheet_rename_title(cuesheet_id, title, album_id):
    album = get_album(album_id)
    piece = get_piece(cuesheet_id)
    cuesheet_path = os.path.join(album['Path'], piece['Name'])
    cuesheet = get_full_cuesheet(cuesheet_path, cuesheet_id)
    cuesheet['Title'] = title
    cuesheet['cue']['title'] = title
    # out_path = os.path.join(album['Path'], 'temp_' + piece['Name'])
    write_full_cuesheet(cuesheet_path, cuesheet)
    return cuesheet_path + ' written'
