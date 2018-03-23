from inspect import currentframe

from website.lib.color import ColorPrint
from music.settings import SKIP_DIRS, MUSIC_FILES
from website.services.services import get_extension

"""flac

"""
import os
from website.db.fetch import (
    get_album_count_by_path,  # get_album_by_path,
    get_componist_path_c, get_album_path_by_id,
    get_componist_path_by_id, get_componist_id_from_album)
from website.db.insert import (
    insert_album, insert_piece, insert_componist,
)
# from website.db.update import set_album_title
from website.db.connect import connect
from website.scripts.helper.rename import (
    rename_cover, restore_cover, sanatize_haakjes, rename_to_back, rename_all_titles,
)
from website.scripts.helper.insert import (
    insert_artiest, insert_composer, insert_componist_by_id, insert_performer_by_id,
)


def insert_pieces(path, album_id, conn, c):
    for ext in MUSIC_FILES:
        for f in os.listdir(path):
            if ext == get_extension(f):
                insert_piece(
                    name=f,
                    code='',  # kirkpatrick(f, 'K ', ' '),
                    album_id=album_id,
                    c=c,
                    conn=conn)


def process_pieces(path, album_id):
    conn, c = connect()
    insert_pieces(path, album_id, conn, c)


def process_album(path, componist_id=None, mother_id=None, is_collectie=0):
    """
    haal stukken (cuesheets en music files) op voor een album
    """
    # if len(path.split('[')) > 1:
    #     print('from: ' + __file__, currentframe().f_lineno)
    #     ColorPrint.print_c('cue_path mag geen accolades of vierkante haken bevatten - quitting', ColorPrint.RED)
    #     return -1
    count = 0
    for ext in MUSIC_FILES:
        for f in os.listdir(path):
            if ext == get_extension(f):
                count += 1
    if count == 0:
        print('from: ' + __file__, currentframe().f_lineno)
        ColorPrint.print_c('No music files in this directory - quitting',
                           ColorPrint.RED)
        return

    conn, c = connect()
    w = path.split('/')
    album_title = w[-1].replace("_", " ")
    album_id = insert_album(
        title=album_title,
        path=path,
        is_collectie=is_collectie,
        c=c,
        conn=conn,
        album_id=mother_id,
    )[0]
    print('from: ' + __file__, currentframe().f_lineno)
    ColorPrint.print_c("created album id: {}".format(album_id), ColorPrint.LIGHTCYAN)
    insert_pieces(path, album_id, conn, c)
    if componist_id:
        insert_componist_by_id(componist_id, c, conn, album_id)
    conn.close()
    return album_id


def count_album_by_path(p):
    conn, c = connect()
    found = get_album_count_by_path(p, c, conn)
    return found['Count']


def process_a(p, mother_id, iscollectie, step_in):
    '''
    Lees in directory p alle stukken in voor een album, onthoud album_id als
    mother. Als step_in waar is, doe hetzelfde in de subdirectories
    (1 niveau diep) met album_id als mother.
    '''
    album_id = process_album(p, mother_id, iscollectie)
    if step_in:
        # one recursive step
        for d2 in os.listdir(p):
            p2 = u'{}/{}'.format(p, d2)
            if os.path.isdir(p2) and d2 not in SKIP_DIRS:
                album_id2 = process_album(p2, album_id, 0)
                if step_in == 2:
                    # second recurisve step
                    for d3 in os.listdir(p2):
                        p3 = u'{}/{}'.format(p, d3)
                        if os.path.isdir(p3) and d3 not in SKIP_DIRS:
                            process_album(p3, album_id2, 0)


def get_album_groups(path, mother_id, iscollectie, step_in):
    '''
    Behandel het path als plaats waar de subdirectories groepen albums bevatten
    '''
    for d in os.listdir(path):
        p = u'{}/{}'.format(path, d)
        if os.path.isdir(p) and d not in SKIP_DIRS:
            process_a(p, mother_id, iscollectie, step_in)


def get_albums(path, mother_id, iscollectie):
    '''
    Behandel het path als plaats waar de albums staan
    '''
    for d in os.listdir(path):
        p = u'{}/{}'.format(path, d)
        if os.path.isdir(p) and d not in SKIP_DIRS:
            process_album(p, mother_id, iscollectie)


def rename_titles(path):
    conn, c = connect()
    rename_all_titles(path, SKIP_DIRS, c, conn)


def get_path_of_componist(componist_id):
    if componist_id is None:
        ColorPrint.print_c('No componist ID given, so quitting', ColorPrint.RED)
        return
    conn, c = connect()
    return get_componist_path_c(componist_id, c)


def get_path_of_album(album_id):
    if album_id is None:
        ColorPrint.print_c('No album ID given, so quitting', ColorPrint.RED)
        return
    conn, c = connect()
    return get_album_path_by_id(album_id, c)


def get_path_by_albumid(album_id):
    conn, c = connect()
    return get_album_path_by_id(album_id, c)


def get_path_by_componistid(album_id):
    conn, c = connect()
    return get_componist_path_by_id(album_id, c)


def open_finder_album(album_id):
    path = get_path_by_albumid(album_id)
    os.system('open "{}"'.format(path))


def open_finder_componist(componist_id):
    path = get_path_by_componistid(componist_id)
    os.system('open "{}"'.format(path))


def from_path(path):
    if path is None:
        raise Exception('No path given')
    w = path.split('/')
    return w[-1]


def insert_composer2(name):
    conn, c = connect()
    return insert_componist(name, c, conn)


def componist_from_album(album_id):
    conn, c = connect()
    cid = get_componist_id_from_album(album_id, c)
    return cid


def main():
    # Init
    componist_id = None
    mother_id = None
    path = None
    album_id = None

    # open_finder_album(album_id=4286)
    # open_finder_componist(ComponistID)
    # return
    # path = get_path_of_componist(ComponistID)
    # album_id = 674
    # path = get_path_of_album(album_id)
    mother_id = 2194
    componist_id = 9
    # componist = from_path(path)
    # ComponistID = componist_from_album(album_id)
    path = '/Volumes/Media/Audio/Klassiek/Collecties/Wanda Landowska - The complete european recordings (1928-1940)'
    ColorPrint.print_c(path, ColorPrint.LIGHTCYAN)
    if path is None:
        print('No path')
        return
    # process_pieces(path, album_id=album_id)
    # return

    # sanatize_haakjes(path, True)
    # restore_cover(path=path, step_in=True)
    # rename_cover(path=path, step_in=True)
    # rename_titles(path)
    # rename_to_back(path)
    process_a(p=path, mother_id=None, iscollectie=1, step_in=1)
    # get_albums(path=path, mother_id=None, iscollectie=0)
    # get_album_groups(path=path, mother_id=album_id, iscollectie=0, step_in=0)
    # process_album(path=path, componist_id=componist_id,
    #               mother_id=mother_id, is_collectie=0)


if __name__ == '__main__':
    main()
