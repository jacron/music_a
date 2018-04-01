import os

from six.moves.urllib.request import urlopen
from channels import Group
from django.conf import settings

from website.lib.color import ColorPrint
from website.scripts.flacs import process_album
from website.scripts.rename import rename_music_files
from website.services.tag import set_metatags, \
    remove_tag, tag_set_metatag, tag_remove_metatag, tag_put_picture
from ..db.fetch import get_piece, get_album
from ..db.insert import abs_insert_componist
from ..db.pieces import refetch_pieces
from ..db.update import update_played, update_piece_library_code, \
    update_librarycode, add_componist_to_album, new_componist, \
    add_new_componist_to_album, remove_componist_from_album, \
    update_componistname, update_componistbirth, update_componistdeath, \
    add_performer_to_album, new_performer, add_new_performer_to_album, \
    remove_performer_from_album, update_performername, update_performerbirth, \
    update_performerdeath, add_instrument_to_album, new_instrument, \
    remove_instrument_from_album, add_new_instrument_to_album, \
    add_tag_to_album, \
    new_tag, remove_tag_from_album, delete_album, read_albums, \
    update_album_title, update_album_description, adjust_kk, inherit_elements, \
    toggle_setting, delete_album_ape, update_db_piece_name
from ..services.album_content import get_website
from ..services.clipboard import delete_score_fragment
from ..services.clipboard import save_score_fragment, save_person
from ..services.export import export_albums
from ..services.makecuesheet import make_cuesheet, rename_cuesheet, \
    make_subs_cuesheet, split_cued_file, edit_cuesheet, combine_sub_cuesheets, \
    norm_cuesheet, remove_cuesheet, split_one_cue_album, split_cue_album, \
    cuesheet_rename_title, cuesheet_title_from_filename
from ..services.path import path_from_id_field, get_path
from ..services.services import openpath, openterminal, pauseplay, opentageditor


def controlplayer(mode):
    if mode == 'pause':
        pauseplay()


def play(args):
    piece = get_piece(args)
    album = get_album(piece['AlbumID'])
    path = album['Path']
    name = piece['Name']
    os.system('open -a "{}" "{}"'.format(settings.MEDIA_PLAYER,
                                         "{}/{}".format(path, name)))
    update_played(piece['ID'])


def path_for_person(path):
    return '{}/person.jpg'.format(path)


def write_file_from_url(url, path):
    f = urlopen(url)
    contents = f.read()
    # response = requests.get(url)
    # contents = open(response[0]).read()
    f = open(path_for_person(path), 'wb')
    f.write(contents)
    f.close()


def person_by_url(post):
    path = path_from_id_field(post)
    if path:
        write_file_from_url(post['url'], path)


def openfinder(objectid, kind):
    path = get_path(objectid, kind)
    if path:
        openpath(path)


def openterm(objectid, kind):
    path = get_path(objectid, kind)
    if path:
        openterminal(path)


def openwebsite(album_id):
    album = get_album(album_id)
    path = get_website(album['Path'])
    if path:
        openpath(path)


def paste_score_fragment(code):
    return save_score_fragment(code)


def remove_score_fragment(code):
    return delete_score_fragment(code)


def paste_person(person_id, person_type):
    return save_person(person_id, person_type)


def add_code(piece_id, librarycode):
    update_piece_library_code(piece_id, librarycode)


def remove_code(piece_id):
    update_piece_library_code(piece_id, None)


def toggle_code_favorite(librarycode, favorite):
    state = {
        'true': 1,
        'false': 0
    }
    update_librarycode(librarycode, state[favorite])


def title2tag(album_id, mode):
    return set_metatags(album_id, mode)


def delete_ape(album_id):
    delete_album_ape(album_id)
    return 'deleted ape'


def remove_tag_titles(album_id):
    return remove_tag(album_id, 'title')


def set_tag_picture(album_id):
    return tag_put_picture(album_id)


def tageditoralbum(album_id):
    path = get_path(album_id, 'album')
    opentageditor(path)
    return 'editor'


def tageditor(path):
    opentageditor(path)
    return 'editor'


def rename_piece_name(piece_id, piece_name, album_id):
    album = get_album(album_id)
    piece = get_piece(piece_id)
    src = os.path.join(album['Path'], piece['Name'])
    dst = os.path.join(album['Path'], piece_name)
    os.rename(src, dst)


def update_metatag(tag, value, album_id):
    return tag_set_metatag(tag, value, album_id)


def remove_metatag(tag, album_id):
    return tag_remove_metatag(tag, album_id)


def update_cuesheet_title(cuesheet_id, title, album_id):
    return cuesheet_rename_title(cuesheet_id, title, album_id)


def update_piece_name(piece_id, piece_name, album_id):
    try:
        rename_piece_name(piece_id, piece_name, album_id)
        update_db_piece_name(piece_id, piece_name)
    except Exception as ex:
        ColorPrint.print_c(str(ex), ColorPrint.CYAN)


def upload(path, componist_id, performer_id, mother_id, is_collection):
    print(path, componist_id, performer_id, mother_id, is_collection)
    collection = 1
    if is_collection == 'false':
        collection = 0
    album_id = process_album(path=path, componist_id=componist_id,
                             performer_id=performer_id,
                             mother_id=mother_id, is_collectie=collection)
    return album_id


def do_rename_music_files(path):
    return rename_music_files(path)


def do_post(post):
    cmd = post['cmd']
    if cmd == 'test':
        msg = 'Hello world (response on test)'
        Group("chat").send({
            "text": msg,
        })
        return 1

    # componist
    if cmd == 'add_componist':
        return add_componist_to_album(int(post['componistid']),
                                      int(post['albumid']))
    if cmd == 'new_componist':
        componistid = new_componist(post['name'])
        return add_componist_to_album(int(componistid[0]), int(post['albumid']))
    if cmd == 'add_new_componist':
        return add_new_componist_to_album(post['name'], int(post['albumid']))
    if cmd == 'abs_new_componist':
        componist_id = abs_insert_componist(post['name'])
        print(componist_id)
        return componist_id
    if cmd == 'remove_componist':
        return remove_componist_from_album(post['id'], post['albumid'])
    if cmd == 'update_componist_name':
        return update_componistname(post['name'], post['id'])
    if cmd == 'update_componist_birth':
        return update_componistbirth(post['years'], post['id'])
    if cmd == 'update_componist_death':
        return update_componistdeath(post['years'], post['id'])

    # performer
    if cmd == 'add_performer':
        return add_performer_to_album(int(post['performerid']),
                                      int(post['albumid']))

    if cmd == 'new_performer':
        performerid = new_performer(post['name'])
        return add_performer_to_album(int(performerid[0]), int(post['albumid']))
    if cmd == 'add_new_performer':
        return add_new_performer_to_album(post['name'], int(post['albumid']))
    if cmd == 'remove_performer':
        return remove_performer_from_album(post['id'], post['albumid'])
    if cmd == 'update_performer_name':
        return update_performername(post['name'], post['id'])
    # if cmd == 'update_performer_years':
    #     return update_performeryears(post['years'], post['id'])
    if cmd == 'update_performer_birth':
        return update_performerbirth(post['years'], post['id'])
    if cmd == 'update_performer_death':
        return update_performerdeath(post['years'], post['id'])

    # instrument
    if cmd == 'add_instrument':
        return add_instrument_to_album(int(post['instrumentid']),
                                       int(post['albumid']))
    if cmd == 'new_instrument':
        instrumentid = new_instrument(post['name'])
        return add_instrument_to_album(int(instrumentid[0]),
                                       int(post['albumid']))
    if cmd == 'remove_instrument':
        return remove_instrument_from_album(post['albumid'])
    if cmd == 'add_new_instrument':
        return add_new_instrument_to_album(post['name'], int(post['albumid']))

    # tag
    if cmd == 'add_tag':
        return add_tag_to_album(int(post['tagid']), int(post['albumid']))
    if cmd == 'new_tag':
        tagid = new_tag(post['name'])
        return add_tag_to_album(int(tagid[0]), int(post['albumid']))
    if cmd == 'remove_tag':
        return remove_tag_from_album(post['id'], post['albumid'])

    # album
    if cmd == 'delete_album':
        return delete_album(post['album_id'])
    if cmd == 'refetch':
        return refetch_pieces(post['albumid'])
    if cmd == 'read_albums':
        return read_albums(post['albumid'])

    if cmd == 'url':
        person_by_url(post)
        return 'Person image fetched by url'
    if cmd == 'play':
        play(post['arg'])
        return 'Played'
    if cmd == 'controlplayer':
        controlplayer(post['mode'])
        return 'controled'
    if cmd == 'openpath':
        path = post['path']
        openpath(path)
        return 'opened'
    if cmd == 'openfinder':
        openfinder(post['objectid'], post['kind'])
        return 'Finder opened'
    if cmd == 'openterminal':
        openterm(post['objectid'], post['kind'])
        return 'Terminal opened'
    if cmd == 'exportalbums':
        return export_albums(post['objectid'], post['kind'])
    if cmd == 'openwebsite':
        openwebsite(post['albumid'])
        return 'Website opened'
    if cmd == 'update_album_title':
        return update_album_title(album_id=int(post['albumid']),
                                  title=post['title'])
    if cmd == 'update_album_description':
        return update_album_description(album_id=int(post['albumid']),
                                        description=post['description'])
    if cmd == 'update_piece_name':
        return update_piece_name(post['pieceid'], post['name'], post['albumid'])
    if cmd == 'update_cuesheet_title':
        return update_cuesheet_title(post['id'], post['title'], post['albumid'])
    if cmd == 'adjust_kk':
        return adjust_kk(album_id=int(post['albumid']))
    if cmd == 'inherit_elements':
        return inherit_elements(post['albumid'])
    if cmd == 'update_metatag':
        return update_metatag(post['tag'], post['value'], post['albumid'])
    if cmd == 'remove_metatag':
        return remove_metatag(post['tag'], post['albumid'])

    # cuesheets
    if cmd == 'makecuesheet':
        return make_cuesheet(post['name'], post.getlist('ids[]'),
                             post['albumid'])
    if cmd == 'renamecue':
        return rename_cuesheet(post['id'], post['albumid'], post['newname'])
    if cmd == 'makesubs':
        return make_subs_cuesheet(post['albumid'])
    if cmd == 'split_cued_file':
        return split_cued_file(post['cue_id'], post['albumid'])
    if cmd == 'split_one_cue_album':
        return split_one_cue_album(post['albumid'])
    if cmd == 'split_cue_album':
        return split_cue_album(post['albumid'])
    if cmd == 'editcuesheet':
        return edit_cuesheet(post['id'], post['albumid'])
    if cmd == 'cuesheet_title_from_filename':
        return cuesheet_title_from_filename(post['id'], post['albumid'])
    if cmd == 'combinesubs':
        return combine_sub_cuesheets(post['albumid'])
    if cmd == 'normcuesheet':
        return norm_cuesheet(post['id'], post['albumid'])
    if cmd == 'removecuesheet':
        return remove_cuesheet(post['id'], post['albumid'])
    if cmd == 'renamecuesheet':
        return rename_cuesheet(post['id'], post['albumid'], post['newname'])

    if cmd == 'add_code':
        return add_code(post['id'], post['code'])
    if cmd == 'remove_code':
        return remove_code(post['id'])
    if cmd == 'toggle_code_favorite':
        return toggle_code_favorite(post['code'], post['favorite'])

    if cmd == 'paste_score_fragment':
        return paste_score_fragment(post['code'])
    if cmd == 'remove_score_fragment':
        return remove_score_fragment(post['code'])
    if cmd == 'paste_person':
        return paste_person(post['id'],  post['type'])

    if cmd == 'proposals':
        return toggle_setting('show_proposals')

    if cmd == 'upload':
        return upload(post['path'],
                      post['componistId'],
                      post['performerId'],
                      post['motherId'],
                      post['collection'])
    if cmd == 'tageditor':
        return tageditor(post['path'])
    if cmd == 'tageditoralbum':
        return tageditoralbum(post['albumid'])
    if cmd == 'title2tag':
        return title2tag(post['albumid'], post['mode'])
    if cmd == 'delete_ape':
        return delete_ape(post['albumid'])
    if cmd == 'remove_tag_titles':
        return remove_tag_titles(post['albumid'])
    if cmd == 'set_tag_picture':
        return set_tag_picture(post['albumid'])
    if cmd == 'rename_music_files':
        return do_rename_music_files(post['path'])

    print(cmd, 'not a valid cmd')
