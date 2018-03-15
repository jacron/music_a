"""flac

"""
import glob
import os
# importing for stand alone script
# from website.services import dirname, filename
from services.services import dirname, filename

cuesheet_extension = '.cue'

# combine_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/sonaten clavecimbel/Sonatas - Belder/"
# combine_part = ["Disc 1of3", "Disc 2of3", "Disc 3of3", ]
combine_path = "/Volumes/Media/Audio/Klassiek/Componisten/Schnittke/The Alfred Schnittke Edition"


def move_file(filepath, nr):
    target = dirname(filepath) + '/' + nr + filename(filepath)
    print(filepath)
    print(target)
    # os.rename(file, target)


def move_file_up(f):
    target = "{}/{}".format(dirname(f), filename(f))
    print(f)
    print(target)
    os.rename(f, target)


def combine():
    print(combine_path)
    files = []

    # for album in combine_part:
        # nr = album.split()[1][0]
        # p = combine_path + album + flac_wild
        # print(p)
        # [move_file(f, nr) for f in glob.iglob(p)]
    # for dir in glob.iglob(combine_path):
    for dir in os.listdir(combine_path):
        # d = dir[0]
        if dir not in ('website', 'cache.dirs'):
            # print(dir)
            p = "{}/{}/*".format(combine_path, dir)
            # print(p)
            for f in glob.iglob(p):
                extension = f.split('.')[-1]
                # print(extension)
                if extension in ('flac', 'cue', 'ape'):
                    files.append(f)
    print(files)
    for f in files:
        move_file_up(f)


def main():
    combine()

if __name__ == '__main__':
    main()
