import json

# from ..db import (
#     get_tags,
#     get_componisten_typeahead, get_performers_typeahead, get_instruments_typeahead,
#     get_general_search, get_album_by_path, connect, get_element)
from ..db.connect import connect
from ..db.fetch import get_tags, get_componisten_typeahead, \
    get_performers_typeahead, get_instruments_typeahead, get_general_search, \
    get_album_by_path, get_element, get_componist_albums, get_album_albums, \
    get_album_by_id, get_collections_typeahead, get_albums_by_cql


def do_get(get):
    cmd = get['cmd']
    if cmd == 'albums_componist':
        albums = get_componist_albums(get['componistId'])
        return json.dumps(albums)
    if cmd == 'cql_search':
        cql = json.loads(get['cql'])
        albums = get_albums_by_cql(cql, 'flat')
        return json.dumps(albums)
    if cmd == 'album_albums':
        albums = get_album_albums(get['albumId'])
        return json.dumps(albums)
    if cmd == 'album_by_id':
        album = get_album_by_id(get['id'])
        return json.dumps(album)
    if cmd == 'tags':
        return json.dumps(get_tags())
    if cmd == 'componisten':
        return json.dumps(get_componisten_typeahead(get.get('format')))
    if cmd == 'performers':
        return json.dumps(get_performers_typeahead(get.get('format')))
    if cmd == 'collections':
        return json.dumps(get_collections_typeahead())
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
