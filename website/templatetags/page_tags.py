from django.template import Library

from . import MENU_ITEMS
from website.services.services import alfabet as alph


register = Library()


@register.inclusion_tag(
    'tagtemplates/albumtags.html'
)
def album_tags(album_metatag_titles, album_metatags):
    return dict(album_metatag_titles=album_metatag_titles,
                album_metatags=album_metatags)


@register.inclusion_tag(
    'tagtemplates/navbar.html',
    takes_context=True
)
def navbar(context):
    request = context['request']
    context['menu'] = MENU_ITEMS
    context['menu_active'] = request.path
    return context


@register.inclusion_tag(
    'tagtemplates/albumlist.html',
    takes_context=True
)
def albumlist(context, albums, list_id=None, list_name=None, cmd=None):
    context['albums'] = albums
    context['list_id'] = list_id
    context['list_name'] = list_name
    context['cmd'] = cmd
    return context


@register.inclusion_tag(
    'tagtemplates/cuesheetlist.html',
)
def cuesheetlist(cuesheets, valid):
    return dict(cuesheets=cuesheets, valid=valid)


@register.inclusion_tag(
    'tagtemplates/pieceslist.html',
)
def pieceslist(pieces):
    wild = None
    if len(pieces) and pieces[0].get(2):
        code = pieces[0].get(2)
        code_parts = code.split(' ')
        if len(code_parts) > 1:
            wild = code_parts[0] + '%'
    return dict(pieces=pieces, wild=wild)


@register.inclusion_tag(
    'tagtemplates/pages.html',
)
def pages(prev_id, next_id, list_title, list_name, list_id, album_id=None):
    return dict(prev_id=prev_id, next_id=next_id, list_title=list_title,
                list_name=list_name, list_id=list_id, album_id=album_id)


@register.inclusion_tag(
    'tagtemplates/cpages.html',
)
def cpages(prev_id, next_id, list_title, wild):
    return dict(prev_id=prev_id, next_id=next_id, list_title=list_title,
                wild=wild)


@register.inclusion_tag(
    'tagtemplates/album_instrument_list.html',
)
def album_instrument_list(album_instrument):
    return dict(album_instrument=album_instrument)


@register.inclusion_tag(
    'tagtemplates/album_collection_list.html',
)
def album_collection_list(album, mother_title):
    return dict(album=album, mother_title=mother_title)


@register.inclusion_tag(
    'tagtemplates/componistenlist.html',
    takes_context=True
)
def componistenlist(context, items):
    context['items'] = items
    return context


@register.inclusion_tag(
    'tagtemplates/performerslist.html',
    takes_context=True
)
def performerslist(context, items):
    context['items'] = items
    return context


@register.inclusion_tag(
    'tagtemplates/editalbum.html',
)
def editalbum(select, add, albumid, options):
    return dict(select=select, add=add, albumid=albumid, options=options)


@register.inclusion_tag(
    'tagtemplates/proposallist.html',
)
def proposallist(proposals, artists, show):
    return dict(proposals=proposals, artists=artists, show=show)


@register.inclusion_tag(
    'tagtemplates/album_controls.html',
)
def album_controls(album_id, website):
    return dict(album_id=album_id, website=website)


@register.inclusion_tag(
    'tagtemplates/upload_controls.html',
)
def upload_controls():
    return dict()


@register.inclusion_tag(
    'tagtemplates/persons_list.html',
)
def persons_list(persons, url, ptype):
    return dict(persons=persons, person_url=url, type=ptype)


@register.inclusion_tag(
    'tagtemplates/alfabet.html',
)
def alfabet():
    return dict(letters=alph())


@register.filter(name='unescape')
def unescape(val):
    unescape.is_safe = True
    # if isinstance(val, str):
    #     return val.encode('string-escape')
    # else:
    return val
