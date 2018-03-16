from django.http import HttpResponse
from django.template import loader

from ..db.fetch import (get_setting, get_codes, get_scarlatti_k_pieces,
                        get_scarlatti, get_bach_k_pieces, get_widow_albums,
                        get_apeflac_albums, get_pathdoubles_albums,
                        get_apealone_albums)
from ..db.update import toggle_setting


def extra_view(request, albums=None, cmd=None):
    template = loader.get_template('website/extra.html')
    rc = get_setting('read_cuesheet')
    sp = get_setting('show_proposals')
    codes = get_codes()
    return HttpResponse(template.render(
        {
            'read_cuesheet': rc['VALUE'],
            'show_proposals': sp['VALUE'],
            'albums': albums,
            'codes': codes,
            'cmd': cmd,
        }, request))


def extra(request):
    return extra_view(request)


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


def cmd_view(request, cmd_code):
    if cmd_code == 'scarlatti':
        return list_scarlatti(request)
    if cmd_code == 'bach':
        return list_bach(request)
    if cmd_code == 'cue':
        toggle_setting('read_cuesheet')
        return extra_view(request)
    if cmd_code == 'widows':
        return extra_view(request, get_widow_albums())
    if cmd_code == 'apeflac':
        return extra_view(request, get_apeflac_albums(), 'del_ape')
    if cmd_code == 'apealone':
        return extra_view(request, get_apealone_albums(), 'split')
    if cmd_code == 'pathdoubles':
        return extra_view(request, get_pathdoubles_albums())
    return extra_view(request)
