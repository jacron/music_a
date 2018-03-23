import os

from music.settings import SKIP_DIRS, MUSIC_FILES
from website.db.connect import connect
from website.db.fetch import get_album_by_path
from website.services.services import get_extension


def album_by_path(p):
    conn, c = connect()
    return get_album_by_path(p, c)


def has_musical_files(path):
    for ext in MUSIC_FILES:
        for f in os.listdir(path):
            if ext == get_extension(f):
                return True
    return False


def traverse(p):
    without_album = 0
    with_album = 0
    print(p)
    with open('out/unregisteredalbums.txt', 'w') as out:
        # out.write('')  # initialize
        for root, dirs, files in os.walk(p):
            for d in dirs:
                if d not in SKIP_DIRS and not d.endswith('_files'):
                    p = os.path.join(root, d)  # create full path
                    album = album_by_path(p)
                    if not album and has_musical_files(p):
                        without_album += 1
                        out.write(p + '\n')
                        print(p)
                    else:
                        with_album += 1
    print(without_album, with_album)


def main():
    path = '/Volumes/Media/Audio/Klassiek/Componisten/Bach'
    traverse(path)


if __name__ == '__main__':
    main()
