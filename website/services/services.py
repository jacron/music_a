import os
import subprocess

from website.lib.color import ColorPrint
from music.settings import COMPONIST_PATH, PERFORMER_PATH, TAG_EDITOR, \
    MEDIA_PLAYER_APP


def replace_haakjes(s):
    for ch in ['[', '{']:
        if ch in s:
            s = s.replace(ch, '(')
    for ch in [']', '}']:
        if ch in s:
            s = s.replace(ch, ')')
    return s


def has_haakjes(s):
    # print(s)
    for ch in ['[', '{']:
        if ch in s:
            return True
    for ch in [']', '}']:
        if ch in s:
            return True
    return False


def directory(path):
    # path = path.decode('utf-8')
    w = path.split('/')[:-1]
    image_path = '/'.join(w)
    return image_path


def dirname(ffile):
    return '/'.join(ffile.split('/')[:-2])


def filename(ffile):
    return ffile.split('/')[-1]


def trimextension(ffile):
    ff = ffile.split('.')[:-1]
    return '.'.join(ff)


def get_extension(s):
    """
    return extension of a filename (without leading point)
    :param s: filename
    :return: extension
    """
    return s.split('.')[-1]


def get_filename(s):
    """
    return a filename without extension
    :param s:
    :return:
    """
    return s.split('.')[:-1]


def dequote(line):
    line = line.strip()
    if line.startswith('"'):
        line = line[1:]
    if line.endswith('"'):
        line = line[:-1]
    return line


def splits_comma_naam(naam):
    c_namen = naam.split(',')
    if len(c_namen) > 1:
        c_firstname = c_namen[1].strip()
        c_lastname = c_namen[0].strip()
    else:
        c_firstname = ''
        c_lastname = naam.strip()
    return c_firstname, c_lastname


def splits_naam(naam):
    if len(naam.split(',')) > 1:
        return splits_comma_naam(naam)
    c_namen = naam.split()
    if len(c_namen) > 1:
        c_lastname = c_namen[-1].strip()
        c_firstname = ' '.join(c_namen[:-1]).strip()
    else:
        c_firstname = ''
        c_lastname = naam.strip()
    return c_firstname, c_lastname


def splits_years(years):
    c_years = years.split('-')
    if len(c_years) < 2:
        return years.strip(), ''
    return c_years[0].strip(), c_years[1].strip()


def alfabet():
    return [chr(i) for i in range(ord('a'), ord('z')+1)]


def openpath(path):
    cmd = 'open "{}"'.format(path)
    os.system(cmd)


def opentageditor(path):
    if os.path.exists(path):
        cmd = ['open', '-a', TAG_EDITOR]
        for f in os.listdir(path):
            extension = f.split('.')[-1]
            if extension == 'flac':
                p = '{}/{}'.format(path, f)
                cmd.append(p)

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()
        if len(out) == 0:
            print(err)
    else:
        ColorPrint.print_c('Path does not exist: {}'.format(path),
                           ColorPrint.RED)


def openterminal(path):
    cmd = 'open -a Terminal "{}"'.format(path).encode('UTF-8')
    os.system(cmd)


def subl_path(path):
    cmd = 'subl "{}"'.format(path).encode('UTF-8')
    os.system(cmd)


def runosascript(osascript):
    args = ["osascript", "-e", osascript]
    subprocess.Popen(args)


def controlplayer(cmd):
    keys = None
    if cmd == 'pause':
        keys = '" "'
    if cmd == 'stop':
        keys = '"s" using command down'
    if cmd == 'previous':
        keys = '"l" using command down'
    if  cmd == 'next':
        keys = '"n" using command down'
    if keys:
        cmdplay(keys)
    else:
        print('unknown cmd: ' + cmd)

# def stopplay():
#     osascript = '''
#     tell application \"{}\"\n
#         activate\n
#         tell application \"System Events\" to keystroke \"s\" using command down\n
#     end tell\n
#     '''.format(MEDIA_PLAYER_APP)
#     runosascript(osascript)


def cmdplay(keys):
    # os.system('open -a "{}" /Pause'.format(settings.MEDIA_PLAYER))
    osascript = '''
    tell application \"{}\"\n
        activate\n
        tell application \"System Events\" to keystroke {}\n
    end tell\n
    '''.format(MEDIA_PLAYER_APP, keys)
    # osascript = '''
    # tell application \"{}\" to pause
    # '''.format(MEDIA_PLAYER_APP)
    runosascript(osascript)
