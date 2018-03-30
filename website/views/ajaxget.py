import json

# from ..db import (
#     get_tags,
#     get_componisten_typeahead, get_performers_typeahead, get_instruments_typeahead,
#     get_general_search, get_album_by_path, connect, get_element)
from website.services.album_content import album_context, full_album
from ..db.connect import connect
from ..db.fetch import get_tags, get_componisten_typeahead, \
    get_performers_typeahead, get_instruments_typeahead, get_general_search, \
    get_album_by_path, get_element, get_componist_albums, get_album_albums, \
    get_album_by_id, get_collections_typeahead, get_albums_by_cql, \
    get_componist, get_performer


def do_get(get):
    cmd = get['cmd']
    if cmd == 'albums_componist':
        albums = get_componist_albums(get['componistId'])
        return json.dumps(albums)
    if cmd == 'composer_by_id':
        person = get_componist(get['id'])
        return json.dumps(person)
    if cmd == 'performer_by_id':
        person = get_performer(get['id'])
        return json.dumps(person)
    if cmd == 'cql_search':
        cql = json.loads(get['cql'])
        albums = get_albums_by_cql(cql, 'flat')
        return json.dumps(albums)
    if cmd == 'album_albums':
        albums = get_album_albums(get['albumId'])
        return json.dumps(albums)
    if cmd == 'album_by_id':
        album = full_album(get['id'])
        # album = get_album_by_id(get['id'])
        # album['context'] = album_context(get['id'])
        return json.dumps(album)
    if cmd == 'tags':
        return json.dumps(get_tags())
    if cmd == 'componisten':
        selection = None
        # selection = get.get('selection')
        return json.dumps(get_componisten_typeahead(
            get.get('format'), selection))
    if cmd == 'performers':
        # selection = None
        selection = get.get('selection')
        if selection:
            selection = json.loads(selection)
        return json.dumps(get_performers_typeahead(
            get.get('format'), selection))
    if cmd == 'collections':
        selection = None
        # selection = get.get('selection')
        return json.dumps(get_collections_typeahead(
            selection
        ))
    if cmd == 'instruments':
        return json.dumps(get_instruments_typeahead())
    if cmd == 'generalsearch':
        return json.dumps(get_general_search(get['query']))
    if cmd == 'album_by_path':
        conn, c = connect()
        return json.dumps(get_album_by_path(get['path'], c))
    if cmd == 'element':
        conn, c = connect()
        return json.dumps(get_element(get['albumid'], get['name'], c))
    return json.dumps(cmd + ':cmd unknown')
