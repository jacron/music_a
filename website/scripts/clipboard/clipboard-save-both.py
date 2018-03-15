# https://media.readthedocs.org/pdf/pillow/stable/pillow.pdf
# box 87 is voorbeeldig: 1711 x 730 is voldoende resolutie, i.p.v. 6833 x 2896, tenminste...
from PIL import ImageGrab

from lib.color import ColorPrint

"""
copy pdf to clipboard
save left side to back.jpg
save right side to folder.jpg
"""
backpath = '/Volumes/Media/tmpscan/back.jpg'
folderpath = '/Volumes/Media/tmpscan/folder.jpg'
rug = 170


def save_front(img):
    width = img.size[0]
    height = img.size[1]
    fbox = (width / 2 + rug, 0, width, height)
    front = img.crop(fbox)
    front.save(folderpath)
    ColorPrint.print_c('folder saved!', ColorPrint.BLUE)


def save_back(img):
    width = img.size[0]
    height = img.size[1]
    bbox = (0, 0, width / 2 - rug, height)
    back = img.crop(bbox)
    back.save(backpath)
    ColorPrint.print_c('back saved!', ColorPrint.BROWN)


def save_cb_image():
    ColorPrint.print_c('Grabbing image from clipboard...', ColorPrint.LIGHTCYAN)
    img = ImageGrab.grabclipboard()
    if img:
        print(img.size)
        save_front(img)
        save_back(img)
        # img.save(backpath)
        # img.save(folderpath)
    else:
        ColorPrint.print_c('No image on clipboard!', ColorPrint.RED)


def main():
    save_cb_image()


if __name__ == '__main__':
    main()
