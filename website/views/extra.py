from django.http import HttpResponse
from django.template import loader

from website.services.clipboard import save_cb_image, save_cb_images
from ..db.fetch import (get_setting, get_codes, get_scarlatti_k_pieces,
                        get_scarlatti, get_bach_k_pieces, get_widow_albums,
                        get_apeflac_albums, get_pathdoubles_albums,
                        get_apealone_albums)
from ..db.update import toggle_setting, delete_album_ape


def extra_albums_view(request, albums=None, cmd=None):
    template = loader.get_template('website/extra.html')
    return HttpResponse(template.render(
        {
            'albums': albums,
            'cmd': cmd,
        }, request))


def cue_view(request):
    template = loader.get_template('website/extra.html')
    rc = get_setting('read_cuesheet')
    return HttpResponse(template.render(
        {
            'read_cuesheet': rc['VALUE'],
        }, request))


def extra(request):
    return extra_albums_view(request)


def list_scarlatti(request):
    template = loader.get_template('website/librarycode_pieces.html')
    return HttpResponse(template.render(
        {
            'items': get_scarlatti_k_pieces(),
            'scarlatti': get_scarlatti(),
            'page_title': 'Scarlatti Sonaten (Kirkpatrick nummering)',
        }, request))


def list_bach(request):
    template = loader.get_template('website/librarycode_pieces.html')
    return HttpResponse(template.render(
        {
            'items': get_bach_k_pieces(),
            'page_title': 'Bach Goldberg',
        }, request))


def not_found_view(request, cmd_code):
    template = loader.get_template('website/notfound.html')
    return HttpResponse(template.render({}, request))


def delete_apes(apes):
    for ape in apes:
        if ape['CountApe'] == 1:
            print(str(ape['ID']) + ' to delete')
            delete_album_ape(ape['ID'])


def cmd_view(request, cmd_code):
    apeflac_albums = get_apeflac_albums()
    # delete_apes(apeflac_albums)

    if cmd_code == 'scarlatti':
        return list_scarlatti(request)
    if cmd_code == 'bach':
        return list_bach(request)
    if cmd_code == 'cue':
        toggle_setting('read_cuesheet')
        return cue_view(request)
    if cmd_code == 'widows':
        return extra_albums_view(request, get_widow_albums())
    if cmd_code == 'apeflac':
        return extra_albums_view(request, apeflac_albums, 'del_ape')
    if cmd_code == 'apealone':
        return extra_albums_view(request, get_apealone_albums(), 'split')
    if cmd_code == 'pathdoubles':
        return extra_albums_view(request, get_pathdoubles_albums())
    if cmd_code == 'folder':
        save_cb_image('folder')
        return extra_albums_view(request)
    if cmd_code == 'back':
        save_cb_image('back')
        return extra_albums_view(request)
    if cmd_code == 'folderback':
        save_cb_images('folder', 'back')
        return extra_albums_view(request)
    return not_found_view(request, cmd_code)
