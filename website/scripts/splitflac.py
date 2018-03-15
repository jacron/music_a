# from __future__ import unicode_literals

import glob

import os
import subprocess

from website.scripts.helper.socket import socket_log
from website.lib.color import ColorPrint
from website.services.cuesheet import get_full_cuesheet
from website.services.services import filename

"""
Stel, een cuesheet adresseert een enkel muziekbestand (ape of flac) en verdeelt 
dat in stukken. In dat geval kunnen we het muziekbestand splitsen in de stukken 
van de cuesheet. Dat doet dit script.

Bij het alfabetisch sorteren moet bijv. deel 2 niet op deel 1 van een ander 
muziekstuk volgen. Daarom beginnen de doelbestanden met een volgnummer, 
aangevuld met nul tot twee voorloopnullen. Als er al genummerde flac-bestanden 
aanwezig zijn, wordt er met een sprongetje van 10 doorgenummerd.

De foutafhandeling voorziet in een uitvoer van de fout naar socket_log.
Een succesboodschap wordt eveneens naar socket_log uitgevoerd.

november 2017 - jan h croonen
"""



FFMPEG = 'ffmpeg'


def pad(t):
    if int(t) < 10:
        return '0{}'.format(t)
    return t


def normtime(t):
    # duration
    # hh:mm:ss.ms
    ttt = t.decode().split('.')
    if len(ttt) < 2:
        return None
    ms = int(ttt[1])
    tt = ttt[0].split(':')
    mm = int(tt[1]) + 60 * int(tt[0])
    return '{}:{}:{}'.format(pad(mm), pad(tt[2]), ms)


def to_duration(time):
    # mm:ss:ff
    t = time.split(':')
    try:
        hh = int(int(t[0]) / 60)
        mm = int(int(t[0]) % 60)
        ss = t[1]
        ms = float(t[2]) / 75 * 1000
    except ValueError:
        return None
    return '{}:{}:{}.{}'.format(hh, mm, ss, int(ms))


def timedif(time2, time1):
    # mm:ss:ff
    # 75 frames per second
    t2 = time2.split(':')
    t1 = time1.split(':')
    ff = int(t2[2]) - int(t1[2])
    borrow = 0
    if ff < 0:
        borrow = 1
        ff += 75
    seconden = int(t2[1]) - int(t1[1]) - borrow
    borrow = 0
    if seconden < 0:
        borrow = 1
        seconden += 60
    minuten = int(t2[0]) - int(t1[0]) - borrow
    ms = float(ff) / 75 * 1000
    ms = int(ms) / 10
    return '{}:{}:{}'.format(pad(minuten), pad(seconden), pad(ms))


def split_file(flac, filepath):
    if not flac:
        return
    duration = to_duration(flac['time'])
    if not duration:
        return
    args = [FFMPEG, '-i', filepath, '-ss', duration]
    if flac['duration']:
        flac_duration = to_duration(flac['duration'])
        if flac_duration:
            args += ['-t', flac_duration, ]
        else:
            ColorPrint.print_c('found no duration for ' + flac['path'],
                               ColorPrint.RED)
    args.append(flac['path'])
    ColorPrint.print_c(flac['fname'], ColorPrint.CYAN)
    socket_log(flac['fname'], 'info')
    subprocess.Popen(args)
    # print(p)


def get_flac(strnr, index, track, basedir, tracks, file_duration):
    # track_title = track['title'].replace('/', '_')
    try:
        fname = u'{} {}.flac'.format(strnr, track['title'])
    except ValueError as v:
        ColorPrint.print_c(str(v) + ',' + track['title'], ColorPrint.RED)
        return None
    fname = fname.replace('/', '_')
    outfile = os.path.join(basedir, fname)
    time = track['index']['time']
    if index < len(tracks) - 1:
        time2 = tracks[index + 1]['index']['time']
        duration = timedif(time2, time)
    else:
        if file_duration:
            duration = timedif(file_duration, time)
        else:
            duration = None
    return {
        'path': outfile,
        'fname': fname,
        'time': time,
        'duration': duration,
    }


def get_duration(filepath):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
           '-of', 'default=noprint_wrappers=1:nokey=1', '-sexagesimal',
           filepath]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    if len(out) == 0:
        print(err)
        return None
    return normtime(out)


def tidy_nr(nr):
    strnr = str(nr)
    if nr < 10:
        strnr = '0' + strnr
    if nr < 100:
        strnr = '0' + strnr
    return strnr


def get_max_nr(basedir):
    nr = 0
    files_path = u"{}{}".format(basedir, "/*.flac")
    for f in glob.iglob(files_path):
        fname = filename(f)
        w = fname.split(' ')[0]
        try:
            i = int(w)
            # make nr the max
            if i > nr:
                nr = i
        except ValueError:
            pass
    return nr


def incr_nr(nr):
    # maak een kleine sprong van tien, om de afzonderlijke bron cuesheets te
    # onderscheiden - tenzij we helemaal aan het begin staan
    if nr == 0:
        nr += 1
    else:
        nr += 10
    return nr


def split_flac(cuepath, album_id):
    cuesheet = get_full_cuesheet(cuepath, 0)
    basedir = os.path.dirname(cuepath)
    nr = get_max_nr(basedir)
    nr = incr_nr(nr)

    ColorPrint.print_c(basedir, ColorPrint.GREEN)
    for cfile in cuesheet['cue']['files']:
        filepath = os.path.join(basedir, cfile['name'])
        file_duration = get_duration(filepath)
        if not file_duration:
            ColorPrint.print_c('unknown duration for: ' + filepath,
                               ColorPrint.RED)
            socket_log(
                'ERR:unknown duration for: ' + filepath,
                'error',
                album_id
            )
            continue
        flacs = []
        tracks = cfile['tracks']
        # use index to keep track of when the last track is being processed
        for index, track in enumerate(tracks):
            strnr = tidy_nr(nr)
            flacs.append(get_flac(strnr, index, track, basedir, tracks,
                                  file_duration))
            nr += 1
        for flac in flacs:
            split_file(flac, filepath)
    socket_log('split finished', 'info')
    print('split finished')


def main():
    # split_flac(cuepath)
    pass


if __name__ == '__main__':
    main()
