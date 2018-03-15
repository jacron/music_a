# https://media.readthedocs.org/pdf/pillow/stable/pillow.pdf
# from PIL import ImageGrab

from website.lib.color import ColorPrint

folderpath = '/Volumes/Media/tmp/back.jpg'


def save_cb_image():
    pass
    # img = ImageGrab.grabclipboard()
    # if img:
    #     img.save(folderpath)
    #     ColorPrint.print_c('back saved!', ColorPrint.LIGHTCYAN)


def main():
    save_cb_image()


if __name__ == '__main__':
    main()
