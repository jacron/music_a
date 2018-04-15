import os

from shutil import copyfile

from music.settings import MUSIC_PATHS, PERSON_FILE
from website.db.connect import connect
from website.db.fetch import get_items
from website.lib.color import ColorPrint


def copy_persons(subdir):
    # copy person.jpg for each person from source to destination
    # if subdir in destination not exists, create it
    # componisten and performers all have to have subdirs
    # in order to provide for instances of person.jpg (portraits) of them
    src = MUSIC_PATHS['saturnus']['AUDIO_ROOT'] + subdir
    dst = MUSIC_PATHS['abeel']['AUDIO_ROOT'] + subdir
    count = 0
    for d in os.listdir(src):
        p = os.path.join(src, d)
        q = os.path.join(dst, d)
        if os.path.isdir(p):
            if not os.path.exists(q):
                os.mkdir(q)
            s = os.path.join(p, PERSON_FILE)
            t = os.path.join(q, PERSON_FILE)
            if os.path.exists(s) and not os.path.exists(t):
                # print(s)
                # print(t)
                copyfile(s, t)
                count += 1
    print('done: ' + str(count))


def update_path_person(table, c, con, item_id, item_path,
                       first_name, last_name):
    if not item_path:
        ColorPrint.print_c('no path for: ' + first_name + ' ' + last_name,
                           ColorPrint.RED)
        return
    # take string after last slash and use that for new path
    sl = item_path.rfind('/') + 1
    p = item_path[sl:]
    print(item_id, item_path)
    sql = 'UPDATE ' + table + ' SET Path=? WHERE ID=?'
    c.execute(sql, (p, item_id,)).fetchone()
    con.commit()


def migrate_path_person(table):
    sql = 'SELECT FirstName, LastName, Path, ID FROM ' + table +  \
          ' ORDER BY LastName'
    items = get_items(sql)
    con, c = connect()
    for item in items:
        update_path_person(table, c, con, item[3], item[2], item[0], item[1])


def update_path_album(album_id, album_path, c, con):
    # take AUDIO_ROOT from path
    prefix = MUSIC_PATHS['saturnus']['AUDIO_ROOT']
    p = album_path[len(prefix):]
    # if album_path[:len(prefix)] != prefix:
    #     ColorPrint.print_c(album_id + ': not the prefix found in: ' + album_path,
    #                        ColorPrint.RED)
    #     return
    # print(album_path)
    # print(p)
    # if not os.path.exists(album_path):
    #     ColorPrint.print_c(str(album_id) + ': ' + album_path, ColorPrint.RED)
    sql = 'UPDATE Album SET Path=? WHERE ID=?'
    c.execute(sql, (p, album_id,)).fetchone()
    con.commit()


def migrate_path_album():
    sql = 'SELECT Title, Path, ID FROM Album' +  \
          ' ORDER BY Title'
    items = get_items(sql)
    con, c = connect()
    for item in items:
        update_path_album(item[2], item[1], c, con)
    print('albums: ' + str(len(items)))


def main():
    # migrate_path_person('Componist')
    # migrate_path_person('Performer')
    # copy_persons('Componisten')
    copy_persons('Performers')
    # migrate_path_album()


if __name__ == '__main__':
    main()
