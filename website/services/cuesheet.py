import codecs

from website.db.fetch import get_album, get_piece
from website.lib.color import ColorPrint
from .services import dequote
import os


class Error(Exception):
    pass


class NotFoundError(Error):
    pass


def get_title(data):
    for line in data.split('\n'):
        line = line.strip()
        pos = line.find('TITLE ')
        if pos != -1:
            rest = pos + len('TITLE ')
            line = line[rest:-1]
            return dequote(line)


def get_element(line, prefix):
    pos = line.find(prefix)
    if pos != -1:
        rest = pos + len(prefix)
        result = line[rest:]
        return result
    return None


def replace_haakjes(s):
    for ch in ['[', '{']:
        if ch in s:
            s = s.replace(ch, '(')
    for ch in [']', '}']:
        if ch in s:
            s = s.replace(ch, ')')
    return s


def parse_cuesheet(lines):
    cue = { 'title': None, 'performer': None, 'files': [], 'rem': [], }
    cuefile, cuetrack = None, None
    for line in lines:
        if len(line) < 1:
            continue
        el_rem = get_element(line, 'REM ')
        if el_rem:
            cue['rem'].append(el_rem)
        el_title = get_element(line, 'TITLE ')
        if el_title:
            if cuetrack:
                cuetrack['title'] = replace_haakjes(dequote(el_title))
            else:
                cue['title'] = dequote(el_title)
        el_performer = get_element(line, 'PERFORMER ')
        if el_performer:
            if cuetrack:
                cuetrack['performer'] = dequote(el_performer)
            else:
                cue['performer'] = dequote(el_performer)
        el_file = get_element(line, 'FILE ')
        if el_file:
            if cuefile:
                cue['files'].append(cuefile)
                if cuetrack:
                    cuefile['tracks'].append(cuetrack)
                    cuetrack = None
            # trim WAVE
            pos = el_file.rfind(' ')
            name = el_file[0:pos]
            cuefile = { 'name': dequote(name), 'tracks': [], }
        el_track = get_element(line, 'TRACK ')
        if el_track:
            nr, name = el_track.split()
            if cuetrack:
                cuefile['tracks'].append(cuetrack)
            cuetrack = { 'nr': nr, 'name': name, }
        el_index = get_element(line, 'INDEX ')
        if el_index:
            if cuetrack:
                nr, time = el_index.split()
                cuetrack['index'] = { 'nr': nr, 'time': time, }
    if cuetrack:
        cuefile['tracks'].append(cuetrack)
    if cuefile:
        cue['files'].append(cuefile)
    return cue


def data_full_cuesheet(path):
    data = None
    with open(path, 'r') as f:
        try:
            data = f.read()
        except UnicodeDecodeError as u:
            ColorPrint.print_c("can't read unicode here", ColorPrint.RED)
            ColorPrint.print_c(str(u), ColorPrint.BLUE)
            ColorPrint.print_c('retrying...', ColorPrint.BLUE)
            with open(path, 'r', encoding='latin1') as f:
                try:
                    data = f.read()
                except Exception as e:
                    ColorPrint.print_c(str(e), ColorPrint.BLUE)
    return data


def parse_rem(rem):
    # e.g. 'DISCID E0116A0E'
    discid, asin = None, None
    for r in rem:
        el_rem = get_element(r, 'DISCID ')
        print(el_rem)
        if el_rem:
            discid = dequote(el_rem)
        el_rem = get_element(r, 'ASIN')
        if el_rem:
            asin = dequote(el_rem)
    return discid, asin


def cue_full_cuesheet(data, cue_id, filename):
    try:
        lines = data.split('\n')
        cue = parse_cuesheet(lines)
    except:
        ColorPrint.print_c('*** parse cue failed (utf-8?)', ColorPrint.RED)
        return None
    discid, asin = parse_rem(cue['rem'])
    return {
        'Filename': filename,
        'Title': cue.get('title'),
        'ID': cue_id,
        'cue': cue,
        'discid': discid,
        'asin': asin
    }


def get_full_cuesheet(path, cue_id):
    filename = os.path.split(path)[1]
    filename = ' '.join(filename.split('.')[:-1])
    cuesheet = None
    if os.path.exists(path):
        data = data_full_cuesheet(path)
        if data:
            cuesheet = cue_full_cuesheet(data, cue_id, filename)
    else:
        raise NotFoundError
    return cuesheet
