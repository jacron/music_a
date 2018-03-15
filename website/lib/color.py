class ColorPrint():
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BROWN = '\033[0;33m'  # brown/orange
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    LIGHTGRAY= '\033[0;37m'
    DARKGRAY = '\033[1;30m'
    LIGHTRED = '\033[1;31m'
    LIGHTGREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    LIGHTBLUE = '\033[1;34m'
    LIGHTPURPLE = '\033[1;35m'
    LIGHTCYAN = '\033[1;36m'
    WHITE = '\033[1;37m'
    NC = '\033[0m'  # No Color

    @staticmethod
    def print_c(s, c):
        print(ColorPrint.str_c(s, c))

    @staticmethod
    def str_c(s, c):
        return u'{}{}{}'.format(c, s, ColorPrint.NC)


def main():
    ColorPrint.print_c("Hallo", ColorPrint.LIGHTCYAN)


if __name__ == '__main__':
    main()
