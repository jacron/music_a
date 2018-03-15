"""
http://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux

You can use these ANSI escape codes:

Black        0;30     Dark Gray     1;30
Red          0;31     Light Red     1;31
Green        0;32     Light Green   1;32
Brown/Orange 0;33     Yellow        1;33
Blue         0;34     Light Blue    1;34
Purple       0;35     Light Purple  1;35
Cyan         0;36     Light Cyan    1;36
Light Gray   0;37     White         1;37

"""

# from lib.util import open_in_finder
# from lib.color import ColorPrint
from makemkv import str_now

GREEN = '\033[0;32m'
NC = '\033[0m'  # No Color

BEEP = '\a'

# print("I {}love{} Stack Overflow\n".format(GREEN, NC))
# open_in_finder("/Volumes/Media/Video/Regisseurs/Maurice Pialat/Loulou (1980)")
# response = input("{}{}{}".format(GREEN, "Wilt u doorgaan?(J/n)", NC))

for i in range(32):

    print("\r{} {}".format(i, 2 ** i), end="")

# 1073741824 = 2 ** 30 = 1 gigabyte
print(str_now())
# print(BEEP)

# ColorPrint.print_c("Hi!", ColorPrint.GREEN)
