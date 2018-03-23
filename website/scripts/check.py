import glob
import os
import sqlite3

# from website.services import filename
from music.settings import SKIP_DIRS, MUSIC_FILES
from website.db.fetch import get_album_id_by_path
from website.db.insert import insert_piece, insert_album
from website.lib.color import ColorPrint
from website.scripts.helper.insert import insert_componist_by_id, kirkpatrick
# from website.db import (get_album_id_by_path,
#                           insert_album, insert_piece, )
# from website.scripts.flacs import skipdirs
from website.services.services import filename

db_path = '../../db.sqlite3'
check_out = 'out/check.txt'
componisten_out = 'out/componisten.txt'
present_out = 'out/present.txt'

'''
check how far we are, putting 'albums' in the database
when looking at certain  directories
'''


def output_file(fname, lines):
    s = ''
    for line in lines:
        s += line + '\n'
    with open(fname, b"w") as fp:
        fp.write(s.encode('utf-8'))


def input_file(fname):
    with open(fname, b'r') as fp:
        s = fp.read().decode('utf-8')
    lines = s.split('\n')
    return lines


def getfiles(p, extension):
    return [x for x in glob.iglob(os.path.join(p, '*.' + extension))]


def process(p, c, conn, lines, present):
    count = 0
    for card in MUSIC_FILES:
        files = getfiles(p, card)
        count += len(files)
    if count == 0:
        return
    album = get_album_id_by_path(p, c, conn)
    if not album:
        lines.append(p)
    else:
        present.append(p)


def check(path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    lines = []
    present = []
    count = 0
    for d in os.listdir(path):
        p = '{}/{}'.format(path, d)
        if os.path.isdir(p) and d not in SKIP_DIRS:
            for d2 in os.listdir(p):
                p2 = '{}/{}'.format(p, d2)
                if os.path.isdir(p2) and d2 not in SKIP_DIRS:
                    print(d2)
                    count += 1
                    process(p2, c, conn, lines, present)
    output_file(check_out, lines)
    output_file(present_out, present)
    print('processed: {}'.format(count))


def insert_pieces(path, album_id, conn, c):
    for card in MUSIC_FILES:
        files_path = u"{}{}".format(path, "/*.{}".format(card))
        for f in glob.iglob(files_path):
            print(f)
            insert_piece(
                name=filename(f),
                code=kirkpatrick(f),
                album_id=album_id,
                c=c,
                conn=conn)


def create(path, album_title, cid):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    album_id = insert_album(
        title=album_title,
        path=path,
        album_id=None,
        is_collectie=0,
        c=c,
        conn=conn,
    )[0]
    ColorPrint.print_c("album_id={}".format(album_id), ColorPrint.LIGHTCYAN)
    # cid = get_componist_by_lastname(componist_name, c)[0]
    insert_componist_by_id(cid, c, conn, album_id)
    insert_pieces(path, album_id, conn, c)
    conn.close()


def create_album(path, cc):
    w = path.split('/')
    album_title = w[-1].replace("_", " ")
    componist_name = w[-2]
    componist_id = cc[componist_name]
    # return componist_name
    create(path, album_title, componist_id)


def ontdubbel(persons):
    npersons = []
    for person in persons:
        if person not in npersons:
            npersons.append(person)
    return npersons


def create_componisten(fname):
    lines = input_file(fname)
    componisten = []
    for line in lines:
        if len(line):
            w = line.split('/')
            componist_name = w[-2]
            componisten.append(componist_name)
        cc = ontdubbel(componisten)
        output_file(componisten_out, cc)


def get_componisten_ids(fname):
    lines = input_file(fname)
    cc = {}
    for line in lines:
        if len(line):
            w = line.split(',')
            cc[w[0]] = int(w[1])
    # print(cc)
    return cc


def create_albums():
    cc = get_componisten_ids(componisten_out)
    lines = input_file(check_out)
    # lines = input_file('out/beethoven.txt')
    # test with first line (5026)
    # create_album(lines[0], cc)
    for line in lines:
        if len(line):
            create_album(line, cc)


def main():
    path = "/Volumes/Media/Audio/Klassiek/Componisten"
    check(path)
    # create_componisten(check_out)
    # create_albums()


if __name__ == '__main__':
    main()
