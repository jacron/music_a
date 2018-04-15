# import glob
import os

from music.settings import MUSIC_FILES, AUDIO_ROOT
from website.services.album_content import full_album
from website.services.services import get_extension
from .connect import connect
from .fetch import get_album_path_by_id, get_pieces
from .insert import insert_piece


def refetch_pieces(album_id):
    """
    stukken (pieces en cusheets) opnieuw ophalen
    met behoud van librarycode, dus
    niet opniew ophalen als ze er nog zijn
    :param album_id:
    :return:
    """
    # delete_pieces_of_album(album_id)
    conn, c = connect()
    path = AUDIO_ROOT + get_album_path_by_id(album_id, c)
    delete_pieces(path, album_id, conn, c)
    insert_pieces(path, album_id, conn, c)
    return full_album(album_id)


def delete_pieces(path, album_id, conn, c):
    pieces = get_pieces(album_id)
    for p in pieces:
        from website.db.update import delete_piece
        delete_piece(p['ID'])


def insert_pieces(path, album_id, conn, c):
    for ext in MUSIC_FILES:
        for f in sorted(os.listdir(path)):
            if f[0] != '.' and ext == get_extension(f):
                insert_piece(
                    name=f,
                    code='',  # kirkpatrick(f, 'K ', ' '),
                    album_id=album_id,
                    c=c,
                    conn=conn)


