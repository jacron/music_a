import subprocess

BEEP = '\a'


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def execute_string_with_output(cmd):
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        outs, errs = process.communicate()
        return errs
    except subprocess.CalledProcessError as e:
        print(e)
    return None


def open_in_finder(s):
    try:
        subprocess.Popen(["open", "-R", s])
    except subprocess.CalledProcessError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)


def q(s):
    return '"' + s + '"'


def beep():
    print(BEEP)


def main():
    beep()


if __name__ == '__main__':
    main()
