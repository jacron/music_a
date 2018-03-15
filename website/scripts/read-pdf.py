from PIL import Image, ImageGrab
from PyPDF2 import PdfFileReader

import warnings

warnings.filterwarnings("ignore")


folderpath = '/Volumes/Media/tmp/folder.jpg'
input_pdf = '/Volumes/Media/Audio/Klassiek/Collecties/Great pianists of the 20th century/Box 036 Emil Gilels/scans GP036.pdf'

number = 0


def try_pdf(page, xObject):
    global number
    # input1 = PdfFileReader(open(input_pdf, "rb"))
    # page0 = input1.getPage(0)
    # xObject = page0['/Resources']['/XObject'].getObject()
    xObject = xObject['/Resources']['/XObject'].getObject()

    for obj in xObject:
        if xObject[obj]['/Subtype'] == '/Image':
            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
            data = xObject[obj].getData()
            if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                mode = "RGB"
            else:
                mode = "P"

            if xObject[obj]['/Filter'] == '/FlateDecode':
                img = Image.frombytes(mode, size, data)
                img.save(obj[1:] + ".png")
            elif xObject[obj]['/Filter'] == '/DCTDecode':
                img = open(obj[1:] + ".jpg", "wb")
                img.write(data)
                img.close()
            elif xObject[obj]['/Filter'] == '/JPXDecode':
                img = open(obj[1:] + ".jp2", "wb")
                img.write(data)
                img.close()
                number += 1
        else:
            try_pdf(page, xObject[obj])


def save_cb_image():
    img = ImageGrab.grabclipboard()
    if img:
        img.save(folderpath)
        print('saved!')


def main():
    file = PdfFileReader(open(input_pdf, "rb"))
    try_pdf(input_pdf, file.getPage(0))


if __name__ == '__main__':
    main()
