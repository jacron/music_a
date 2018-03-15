# coding: utf-8
import codecs
import os

# from db import get_componist, get_componist_albums, get_album_albums,
# get_pieces, get_album
from ..db.fetch import get_album, get_pieces, get_album_albums, get_componist, \
    get_componist_albums


def read_children(albums, target):
    lines = []
    for album in albums:
        album_target = os.path.join(target, album['Title'])
        lines.append(u'mkdir -p "{}"'.format(album_target))
        album_o = get_album(album['ID'])
        source = album_o['Path']
        pieces = get_pieces(album['ID'])
        for piece in pieces:
            lines.append(u'cp "{}" "{}"'.format(
                os.path.join(source, piece[0]),
                os.path.join(album_target, piece[0])
            ))
        folder_name = 'folder.jpg'
        back_name = 'back.jpg'
        folder_path = os.path.join(source, folder_name)
        back_path = os.path.join(source, back_name)
        if os.path.exists(folder_path):
            lines.append(u'cp "{}" "{}"'.format(
                folder_path,
                os.path.join(album_target, folder_name)
            ))
        if os.path.exists(back_path):
            lines.append(u'cp "{}" "{}"'.format(
                back_path,
                os.path.join(album_target, 'back.jpg')
            ))

    return lines


def read_mothers(albums, target):
    lines = []
    for album in albums:
        album_target = os.path.join(target, album['Title'])
        # if not os.path.exists(album_target):
        lines.append(u'mkdir -p "{}"'.format(album_target))
        albums = get_album_albums(album['ID'])
        lines += read_children(albums, album_target)
    return lines


def write_script(wpath, lines):
    if len(lines):
        content = ''
        for line in lines:
            content += line + '\n'
        with codecs.open(wpath, 'w', 'utf-8') as f:
            f.write(u'{}'.format(content))


def export_albums(objectid, kind):
    target = '/Volumes/Media/tmp'
    print('creating export script with target=', target)
    wpath = 'export.sh'
    lines = []
    lines.append('#!/usr/bin/env bash')
    if kind == 'componist':
        componist = get_componist(objectid)
        target = os.path.join(target, componist['LastName'])
        lines.append(u'mkdir "{}"'.format(target))
        albums = get_componist_albums(objectid)
        lines += read_children(albums['children'], target)
        lines += read_mothers(albums['mothers'], target)
    write_script(wpath, lines)
