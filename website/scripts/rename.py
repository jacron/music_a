from music.settings import MUSIC_FILES
import os

from website.services.services import get_extension

sample_path = '/Volumes/Media/Audio/Klassiek/Componisten/Mozart/zauberflote/abbado/cd2'
ltrim = ''
l_add = 'B'


def rename_file(path, f):
    src = os.path.join(path, f)
    if len(ltrim) and f[0] == ltrim:
        f = f[1:]
    if len(l_add):
        f = l_add + f
    dst = os.path.join(path, f)
    print(dst)
    os.rename(src, dst)


def rename_music_files(path):
    for ext in MUSIC_FILES:
        for f in os.listdir(path):
            if ext == get_extension(f):
                rename_file(path, f)
    return ''


def main():
    rename_music_files(sample_path)


if __name__ == '__main__':
    main()
