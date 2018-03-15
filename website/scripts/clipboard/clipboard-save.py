# https://media.readthedocs.org/pdf/pillow/stable/pillow.pdf
from PIL import ImageGrab

from website.lib.color import ColorPrint
from website.views.ajaxpost import openpath

folderpath = '/Volumes/Media/tmp/folder.jpg'
path = '/Volumes/Media/tmp'


def save_cb_image():
    img = ImageGrab.grabclipboard()
    if img:
        img.save(folderpath)
        ColorPrint.print_c('front saved!', ColorPrint.LIGHTCYAN)
        openpath(path)
    else:
        ColorPrint.print_c('No image on clipboard!', ColorPrint.RED)


def main():
    # openpath(path)
    save_cb_image()


if __name__ == '__main__':
    main()
