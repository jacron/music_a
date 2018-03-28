from datetime import datetime

import os

# from website.db.update import delete_album_ape
from website.services.services import get_extension
from .connect import connect


def make_fullname(first_name, last_name):
    if not first_name or len(first_name) == 0:
        return last_name
    return u'{} {}'.format(first_name, last_name)


def make_fullname_formatted(first_name, last_name, frmat):
    return frmat.replace('%Last', last_name).replace('%First', first_name)


def print_error(sql, msg):
    print('in db encoding error:', msg)
    print(sql)


def execute(sql, params):
    conn, c = connect()
    try:
        items = c.execute(sql, params).fetchall()
    except:
        print_error(sql, 'execute')
        conn.close()
        return []
    conn.close()
    return items


def get_items_with_parameter(sql, oid):
    conn, c = connect()
    items = []
    try:
        items = c.execute(sql, (oid,)).fetchall()
    except:
        print_error(sql, 'get_items_with_parameters')
    conn.close()
    return items


def get_items_with_2parameter(sql, a, b):
    conn, c = connect()
    items = []
    try:
        items = c.execute(sql, (a, b, )).fetchall()
    except:
        print_error(sql, 'get_items_with_2')
    conn.close()
    return items


def get_items(sql):
    conn, c = connect()
    # items = [item for item in c.execute(sql).fetchall()]
    items = c.execute(sql).fetchall()
    conn.close()
    return items


def get_item_with_id(sql, oid):
    conn, c = connect()
    return c.execute(sql, (oid,)).fetchone()


def named_albums(items):
    out = []
    for item in items:
        out.append({
            'Title': item[0],
            'ID': item[1],
        })
    return out


def get_path_doubles(album):
    sql = '''
      SELECT 
      Title, 
      Album.ID
      FROM Album 
      WHERE Album.Path=?
      AND NOT Album.ID=?
      GROUP BY Title
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_2parameter(sql, album['Path'], album['ID'],)
    return named_albums(items)


def get_album_albums(id_album):
    sql = '''
      SELECT 
      Title, 
      Album.ID, 
      Componist.FirstName, 
      Componist.LastName  
      FROM Album 
      LEFT JOIN Componist_Album ON Componist_Album.AlbumID=Album.ID
      LEFT JOIN Componist ON Componist.ID=Componist_Album.ComponistID
      WHERE Album.AlbumID=?
      GROUP BY Title
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, id_album)
    out = []
    for item in items:
        componist = ''
        if item[2] or item[3]:
            componist = u'{} {}'.format(item[2], item[3])
        out.append({
            'Title': item[0],
            'ID': item[1],
            'Componist': componist,
        })
    return out


sql_albums = {
    """queries that only have to fetch id's but need titles to order correctly.
    these are used for getting next or previous album in a list
    
    """
    'all': '''
      SELECT 
        Title, 
        Album.ID
      FROM Album 
      WHERE Album.AlbumID=?
      GROUP BY Title
      ORDER BY Title COLLATE NOCASE
    ''',
    'componist': '''
      SELECT 
        Title, 
        Album.ID
      FROM Album
       JOIN Componist_Album AS c
       ON c.AlbumID=Album.ID
      WHERE c.ComponistID=?
      GROUP BY Title
      ORDER BY Title COLLATE NOCASE
    ''',
    'performer': '''
      SELECT 
        Title, 
        Album.ID
      FROM Album
       JOIN Performer_Album AS c
       ON c.AlbumID=Album.ID
      WHERE c.PerformerID=?
      GROUP BY Title
      ORDER BY Title COLLATE NOCASE
    ''',
    'tag': '''
      SELECT 
        Title, 
        Album.ID
      FROM Album
       JOIN Tag_Album AS c
       ON c.AlbumID=Album.ID
      WHERE c.TagID=?
      GROUP BY Title
      ORDER BY Title COLLATE NOCASE
    ''',
    'gather': '''
      SELECT 
        Title, 
        Album.ID
      FROM Album
      WHERE IsCollection=2
      GROUP BY Title
      ORDER BY Title COLLATE NOCASE
    '''
}


sql_mother_albums = '''
      SELECT 
        Title, 
        Album.ID
      FROM Album 
      WHERE Album.AlbumID=?
      GROUP BY Title
      ORDER BY Title COLLATE NOCASE
    '''


def get_next_librarycode(librarycode, librarywild):
    if not librarycode : return None
    sql = sql_librarycode.format('')
    items = get_items_with_parameter(sql, librarywild)
    match = None
    for item in items:
        if match:
            return item[0]
        if item[0] == librarycode:
            match = librarycode
    return None


def get_next_album(id_mother, id_album):
    if not id_mother : return None
    items = get_items_with_parameter(sql_mother_albums, id_mother)
    match = None
    for item in items:
        if match:
            return item[1]
        if int(item[1]) == int(id_album):
            match = id_album
    return None


def get_list_album_items(list_name, list_id):
    sql = sql_albums.get(list_name)
    if int(list_id) == 0:
        return get_items(sql)
    else:
        return get_items_with_parameter(sql, list_id)


def get_next_list_album(id_album, list_name, list_id):
    if not list_name or not list_id:
        return None
    items = get_list_album_items(list_name, list_id)
    match = None
    for item in items:
        if match:
            return item[1]
        if int(item[1]) == int(id_album):
            match = id_album
    return None


def get_prev_librarycode(librarycode, librarywild):
    if not librarycode : return None
    sql = sql_librarycode.format('')
    items = get_items_with_parameter(sql, librarywild)
    match = None
    for item in items:
        if match and item[0] == librarycode:
            return match
        match = item[0]
    return None


def get_prev_album(id_mother, id_album):
    if not id_mother : return None
    items = get_items_with_parameter(sql_mother_albums, id_mother)
    match = None
    for item in items:
        if match and int(item[1]) == int(id_album):
            return match
        match = int(item[1])
    return None


def get_prev_list_album(id_album, list_name, list_id):
    if not list_name or not list_id:
        return None
    items = get_list_album_items(list_name, list_id)
    if items:
        match = None
        for item in items:
            if match and int(item[1] == int(id_album)):
                return match
            match = int(item[1])
    return None


def get_albums_by_title(q):
    sql = '''
      SELECT Title, Album.ID, 
        Componist.FirstName, Componist.LastName,
        Tag.Name
      FROM Album 
      JOIN Componist_Album ON Album.ID=Componist_Album.AlbumID
      JOIN Componist ON Componist.ID=Componist_Album.ComponistID
      LEFT JOIN Tag_Album ON Album.ID = Tag_Album.AlbumID
      LEFT JOIN Tag ON Tag.ID = Tag_Album.TagID
      WHERE Title LIKE ?
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, '%' + q + '%')
    out = []
    for item in items:
        out.append({
            'Title': item[0],
            'ID': item[1],
            'Componist': u'{} {}'.format(item[2], item[3]),
            'TagName': item[4],
        })
    return out


def get_albums():
    sql = '''
      SELECT Title, Album.ID, Componist.FirstName, Componist.LastName  
      FROM Album 
      JOIN Componist_Album ON Album.ID=Componist_Album.AlbumID
      JOIN Componist ON Componist.ID=Componist_Album.ComponistID
      WHERE IsCollection ISNULL OR IsCollection=0
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Title': item[0],
            'ID': item[1],
            'Componist': u'{} {}'.format(item[2], item[3]),
        })
    return out


def get_collections():
    sql = '''
      SELECT Title, ID FROM Album
      WHERE IsCollection=1
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items(sql)
    return named_albums(items)


def get_collections_query(query):
    sql = '''
      SELECT Title, ID FROM Album
      WHERE IsCollection=1
      AND Title LIKE ?
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, '%' + query + '%')
    return named_albums(items)


def get_gatherers():
    sql = '''
      SELECT Title, ID FROM Album
      WHERE IsCollection=2
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items(sql)
    return named_albums(items)


def get_pieces(album_id):
    """
    get pieces for album (Name, ID, LibraryCode)
    :param album_id:
    :return:
    """
    sql = '''
      SELECT Name, ID, LibraryCode 
      FROM Piece 
      WHERE AlbumID=?
      ORDER BY Name
    '''
    items = get_items_with_parameter(sql, album_id)
    out = []
    for item in items:
        code = item[2]
        if code == '0':
            code = None
        out.append({
            # 0: item[0],
            # 1: item[1],
            # 2: code,
            'Name': item[0],
            'ID': item[1],
            'LibraryCode': code,
        })
    return out


def named_persons(items):
    out = []
    for item in items:
        out.append({
            'FirstName': item[0],
            'LastName': item[1],
            'FullName': make_fullname(item[0], item[1]),
            'NameFull': u'{}, {}'.format(item[1], item[0]),
            'Path': item[2],
            'Birth': item[3],
            'Death': item[4],
            'ID': item[5],
            'Albums': item[6],
        })
    return out


def get_persons_typeahead(items, format):
    out = []
    for item in items:
        if format:
            out.append({
                'Name': make_fullname_formatted(item[0], item[1], format),
                'ID': item[2],
            })
        else:
            out.append({
                'FullName': make_fullname(item[0], item[1]),
                'LastName': item[1],
                'ID': item[2],
            })
    return out


def get_componisten_typeahead(format):
    sql = '''
      SELECT FirstName, LastName, ID
      FROM Componist
      ORDER BY LastName
    '''
    items = get_items(sql)
    out = get_persons_typeahead(items, format)
    return out


def get_performers_typeahead(format):
    sql = '''
      SELECT FirstName, LastName, ID
      FROM Performer
      ORDER BY LastName
    '''
    items = get_items(sql)
    out = get_persons_typeahead(items, format)
    return out


def get_general_search(query):
    # get album by name, as a simple beginning
    sql = '''
      SELECT Title, ID
      FROM Album
      WHERE Title LIKE ?
      LIMIT 10
    '''
    items = get_items_with_parameter(sql, '%' + query + '%')
    out = []
    for item in items:
        # out.append(item[0])
        out.append({
            'name': item[0],
            'ID': item[1],
        })
    return out


def get_collections_typeahead():
    sql = '''
      SELECT Title, ID
      FROM Album
      WHERE IsCollection=1
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Title': item[0],
            'ID': item[1],
        })
    return out


def get_instruments_typeahead():
    sql = '''
      SELECT Name, ID
      FROM Instrument
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'ID': item[1],
        })
    return out


def get_period_componisten(period):
    pp = period.split('-')
    if len(pp) == 1:
        pmin = period
        pmax = 0
    else:
        if len(pp[0]) < 1:  # e.g. -1900
            pmin = 0
            pmax = pp[1]
        else:
            if len(pp[1]) < 1:  # e.g. 1800-
                pmin = pp[0]
                pmax = 0
            else:
                pmin = pp[0]
                pmax = pp[1]
    sql = '''
    SELECT *
    FROM (
      SELECT
        FirstName,
        LastName,
        C.Path,
        Birth,
        Death,
        C.ID,
        COUNT(A.ID) AS Albums
      FROM Componist C
        LEFT JOIN Componist_Album CA
          ON CA.ComponistID = C.ID
         LEFT JOIN Album A
          ON CA.AlbumID = A.ID
      GROUP BY C.ID
      ORDER BY LastName
    ) WHERE Death > ?
    '''
    if pmax > 0:
        sql += 'AND Death < ?'
        items = get_items_with_2parameter(sql, int(pmin), int(pmax))
    else:
        items = get_items_with_parameter(sql, int(pmin))
    return named_persons(items)


def get_componisten():
    sql = '''
SELECT *
FROM (
  SELECT
    FirstName,
    LastName,
    C.Path,
    Birth,
    Death,
    C.ID,
    COUNT(A.ID) AS Albums
  FROM Componist C
    LEFT JOIN Componist_Album CA
      ON CA.ComponistID = C.ID
     LEFT JOIN Album A
      ON CA.AlbumID = A.ID
  GROUP BY C.ID
  ORDER BY LastName
)
'''
    items = get_items(sql)
    return named_persons(items)


def get_performers():
    sql = '''
      SELECT FirstName, LastName, C.Path, Birth, Death,
        C.ID, COUNT(A.ID) AS Albums
      FROM Performer C
        LEFT JOIN Performer_Album CA
          ON CA.PerformerID = C.ID
        LEFT JOIN Album A
          ON CA.AlbumID = A.ID
      GROUP BY C.ID
      ORDER BY LastName
      '''
    items = get_items(sql)
    return named_persons(items)


def get_instruments():
    sql = '''
      SELECT Name, ID 
      FROM Instrument
      ORDER BY Name
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'ID': item[1],
        })
    return out


def get_componist_aliasses():
    sql = '''
      SELECT Name, ComponistID 
      FROM ComponistAlias
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'ComponistID': item[1],
        })
    return out


def get_performer_aliasses():
    sql = '''
      SELECT Name, PerformerID
      FROM PerformerAlias
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'PerformerID': item[1],
        })
    return out


def get_tags():
    sql = '''
      SELECT Name, ID 
      FROM Tag
      ORDER BY Name COLLATE NOCASE
    '''
    items = get_items(sql)
    out = []
    ln = 0
    for item in items:
        ln += 1
        out.append({
            'Name': item[0],
            'ID': item[1],
        })
    return out


def get_performer_albums(id_performer):
    sql = '''
        SELECT
            Album.Title,
            Album.ID
        FROM Performer_Album
            JOIN Performer ON Performer.ID = Performer_Album.PerformerID
            JOIN Album ON Album.ID = Performer_Album.AlbumID
        WHERE Performer_Album.PerformerID =?
        ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, id_performer)
    return named_albums(items)


def get_tag_albums(id_tag):
    sql = '''
        SELECT
            Album.Title,
            Album.ID
        FROM Tag_Album
            JOIN Tag ON Tag.ID = Tag_Album.TagID
            JOIN Album ON Album.ID = Tag_Album.AlbumID
        WHERE Tag_Album.TagID =?
        ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, id_tag)
    # named_items = named_albums_with_mother(items)
    # return filter_contained_children(named_items)
    out = []
    for item in items:
        out.append({
            'Title': item[0],
            'ID': item[1],
        })
    return out


def named_albums_with_mother(items):
    out = []
    for item in items:
        out.append({
            'Title': item[0],
            'AlbumID': item[1],
            'ID': item[2],
        })
    return out


def filter_contained_children(items):
    # return lists of mothers (with property mother is true) and children
    # N.B. sometimes a mother is a child, i.e. in the children list an album has property mother true
    # but somehow this is right
    # Title, AlbumID, ID
    children = []
    mothers = []
    for album1 in items:
        found = False
        for album2 in items:
            if album2 != album1:
                if album2['ID'] == album1['AlbumID']: # this album has a mother in this list
                    found = True
                    album2['mother'] = True
        if not found:
            if album1.get('mother'):
                mothers.append(album1)
            else:
                children.append(album1)
    for album in children:
        if album.get('mother'):
            mothers.append(album)
            children.remove(album)
    # mothers.sort(key=lambda a: str(album['Title'].lower))
    mothers = sorted(mothers, key=lambda x: x['Title'].lower())
    return {
        'mothers': mothers,
        'children': children
    }


def get_instrument_albums(id_instrument):
    sql = '''
      SELECT 
       Title,
       ID FROM Album
      WHERE InstrumentID=?
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, id_instrument)
    # named_items = named_albums_with_mother(items)
    # return filter_contained_children(named_items)
    out = []
    for item in items:
        out.append({
            'Title': item[0],
            'ID': item[1],
        })
    return out


def get_instrument_albums_search(id_instrument, query):
    sql = '''
      SELECT 
       Title,
       AlbumID,
       ID FROM Album
      WHERE InstrumentID=?
      AND Title LIKE ?
      ORDER BY Title COLLATE NOCASE
    '''
    items = get_items_with_2parameter(sql, id_instrument, '%' + query + '%')
    named_items = named_albums_with_mother(items)
    return filter_contained_children(named_items)


def get_componist_albums(id_componist):
    sql = '''
        SELECT
            Album.Title,
            Album.AlbumID,
            Album.ID
        FROM Componist_Album
            JOIN Componist ON Componist.ID = Componist_Album.ComponistID
            JOIN Album ON Album.ID = Componist_Album.AlbumID
        WHERE Componist_Album.ComponistID =?
        ORDER BY Album.Title COLLATE NOCASE
    '''
    items = get_items_with_parameter(sql, id_componist)
    named_items = named_albums_with_mother(items)
    return filter_contained_children(named_items)


def get_componist_albums_query(id_componist, query):
    if not query : return get_componist_albums(id_componist)
    sql = '''
        SELECT
            Album.Title,
            Album.AlbumID,
            Album.ID
        FROM Componist_Album
            JOIN Componist ON Componist.ID = Componist_Album.ComponistID
            JOIN Album ON Album.ID = Componist_Album.AlbumID
        WHERE Componist_Album.ComponistID =?
        AND Album.Title LIKE ?
        ORDER BY Album.Title COLLATE NOCASE
    '''
    items = get_items_with_2parameter(sql, id_componist, '%' + query + '%')
    named_items = named_albums_with_mother(items)
    return filter_contained_children(named_items)


def get_instrument(id_instrument):
    sql = '''
    SELECT Name, ID FROM Instrument WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_instrument)
    return {
        "Name": fields[0],
        "ID": fields[1]
    }


def get_performer_path(id_performer):
    sql = '''
    SELECT Path FROM Performer WHERE ID=?
    '''
    item = get_item_with_id(sql, id_performer)
    if item:
        return item[0]
    return None


def get_componist_path(id_componist):
    sql = '''
    SELECT Path 
    FROM Componist WHERE ID=?
    '''
    item = get_item_with_id(sql, id_componist)
    if item:
        return item[0]
    return None


def add_to_where(where_sql, cql, parameter_list, parameters):
    if len(where_sql) == 0:
        where_sql = ' WHERE '
    else:
        where_sql += ' AND '
    list = parameter_list.split(',')
    if len(list) == 1:
        cql = cql.format('?')
        parameters.append(parameter_list)
    else:
        placeholders = ''
        for arg in list:
            if len(placeholders):
                placeholders += ','
            placeholders += '?'
            parameters.append(arg)
        cql = cql.format(placeholders)
    where_sql += cql
    return where_sql


def process_cql(cql):
    parameters = []
    where_sql = ''
    sql = ''
    if cql.get('componist'):
        sql += '''
            JOIN Componist_Album ON Componist_Album.AlbumID = A.ID 
        '''
        where_sql = add_to_where(
            where_sql,
            'Componist_Album.ComponistID IN ({})',
            cql.get('componist'),
            parameters
        )
    if cql.get('performer'):
        sql += '''
            JOIN Performer_Album ON Performer_Album.AlbumID = A.ID
        '''
        where_sql = add_to_where(
            where_sql,
            'Performer_Album.PerformerID IN ({})',
            cql.get('performer'),
            parameters)
    if cql.get('tag'):
        sql += '''
            JOIN Tag_Album ON Tag_Album.AlbumID = A.ID
        '''
        where_sql = add_to_where(
            where_sql,
            'Tag_Album.TagID IN ({})',
            cql.get('tag'), parameters)
    if cql.get('instrument'):
        where_sql = add_to_where(
            where_sql,
            'A.InstrumentID IN ({})',
            cql.get('instrument'),
            parameters)
    if cql.get('title'):
        where_sql = add_to_where(
            where_sql,
            'A.Title LIKE {}',
            '%' + cql.get('title') + '%',
            parameters)
    if cql.get('mother'):
        where_sql = add_to_where(
            where_sql,
            'A.AlbumID IN ({})',
            cql.get('mother'),
            parameters)
    return parameters, where_sql, sql


def get_albums_by_cql(cql, mode='deep'):
    """
    our semi query language contains id's for several elements
    these id's can be multiple, comma-seperated values
    :param cql: dict
    :param mode: string 'deep' | 'flat'
    :return: albums in groups (mother- and children albums)
    """
    parameters, where_sql, sql = process_cql(cql)
    if len(where_sql):
        sql = '''
            SELECT
                A.Title,
                A.AlbumID,
                A.ID
            FROM Album A''' + sql + where_sql
        sql += '''
        ORDER BY A.Title COLLATE NOCASE
        '''
        conn, c = connect()
        items = []
        try:
            items = c.execute(sql, parameters).fetchall()
        except:
            print_error(sql, 'get_albums_by_cql')
        conn.close()
        named_items = named_albums_with_mother(items)
        if mode == 'deep':
            grouped_items = filter_contained_children(named_items)
            return grouped_items
        else:
            return named_items
    return {}


def get_codes():
    sql = '''
    SELECT LibraryCode, Explanation, Range, M FROM (
        SELECT LibraryCode, Explanation, Range, 
          CAST(substr(Range, 0, instr(Range, '-')) AS INT) M
          FROM Librarycode_Explanation
    )
    ORDER BY LibraryCode, M
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Code': item[0],
            'Description': item[1],
            'Range': item[2],
        })
    return out


def get_componist(id_componist):
    sql = '''
    SELECT FirstName, LastName, Birth, Death, Path, ID 
    FROM Componist WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_componist)
    if not fields:
        return {}
    return {
        "FirstName": fields[0],
        "LastName": fields[1],
        "FullName": make_fullname(fields[0], fields[1]),
        "Birth": fields[2],
        "Death": fields[3],
        "Path": fields[4],
        "ID": fields[5],
    }


def get_album_instruments(id_album):
    sql = '''
    SELECT Name, Instrument.ID 
    FROM Instrument
    JOIN Album ON Album.InstrumentID = Instrument.ID
    WHERE Album.ID = ?
    '''
    fields = get_item_with_id(sql, id_album)
    if fields:
        return {
            "Name": fields[0],
            "ID": fields[1],
        }
    else:
        return {}


def get_album_tags(id_album):
    sql = '''
        SELECT
            Name,
            Tag.ID
        FROM Tag_Album
            JOIN Tag ON Tag.ID = Tag_Album.TagID
            JOIN Album ON Album.ID = Tag_Album.AlbumID
        WHERE Tag_Album.AlbumID =?
    '''
    items = get_items_with_parameter(sql, id_album, )
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'ID': item[1],
        })
    return out


def get_album_performers(id_album):
    sql = '''
        SELECT
            FirstName,
            LastName,
            Birth,
            Death,
            Performer.ID
        FROM Performer_Album
            JOIN Performer ON Performer.ID = Performer_Album.PerformerID
            JOIN Album ON Album.ID = Performer_Album.AlbumID
        WHERE Performer_Album.AlbumID =?
    '''
    items = get_items_with_parameter(sql, id_album, )
    out = []
    for item in items:
        out.append({
            'FirstName': item[0],
            'LastName': item[1],
            'FullName': make_fullname(item[0], item[1]),
            'Birth': item[2],
            'Death': item[3],
            'ID': item[4],
        })
    return out


def get_album_componisten(id_album):
    sql = '''
        SELECT
            FirstName,
            LastName,
            Birth,
            Death,
            Componist.ID
        FROM Componist_Album
            JOIN Componist ON Componist.ID = Componist_Album.ComponistID
            JOIN Album ON Album.ID = Componist_Album.AlbumID
        WHERE Componist_Album.AlbumID =?
    '''
    items = get_items_with_parameter(sql, id_album, )
    out = []
    for item in items:
        out.append({
            'FirstName': item[0],
            'LastName': item[1],
            'FullName': make_fullname(item[0], item[1]),
            'Birth': item[2],
            'Death': item[3],
            'ID': item[4],
        })
    return out


def get_setting(name):
    sql = '''
    SELECT VALUE
    FROM Settings
    WHERE Name=?
    '''
    conn, c = connect()
    fields = c.execute(sql, (name, )).fetchone()
    return {
        'VALUE': fields[0],
    }


def get_scarlatti():
    sql = '''
    SELECT FirstName, LastName, ID
    FROM Componist
    WHERE FirstName='D'
    AND LastName='Scarlatti'
    '''
    conn, c = connect()
    fields = c.execute(sql).fetchone()
    return {
        'FullName': make_fullname(fields[0], fields[1]),
        'ID': fields[2],
    }


def delete_not_existing_path_albums(items):
    for item in items:
        if not os.path.exists(item[2]):
            print(item[0], ' path does not exist')
            from db.update import delete_album
            delete_album(item[1])


def get_pathdoubles_albums():
    sql = '''
SELECT Title, ID, Path, c
FROM (
  SELECT
    TITLE,
    ID,
    PATH,
    COUNT(*) AS c
  FROM Album
  GROUP BY Path
  ORDER BY Path
)
WHERE c > 1;
    '''
    conn, c = connect()
    items = c.execute(sql).fetchall()
    conn.close()
    out = []
    for item in items:
        out.append({
            'Title': item[0],
            'ID': item[1],
            'Path': item[2],
            'Count': item[3],
        })
    return out


def get_apeflac_albums():
    sql = '''
    SELECT Title, ID, Path
    FROM Album 
        '''
    conn, c = connect()
    items = c.execute(sql).fetchall()
    conn.close()
    out = []
    for item in items:
        pieces = get_pieces(item[1])
        count_ape = 0
        count_flac = 0
        for piece in pieces:
            ext = get_extension(piece['Name'])
            if ext == 'flac':
                count_flac += 1
            if ext == 'ape':
                count_ape += 1
        if count_ape > 0 and count_flac > 0:
            it = {
                'Title': item[0],
                'ID': item[1],
                'Path': item[2],
                'CountApe': count_ape,
                'CountFlac': count_flac,
            }
            out.append(it)
    return out


def get_apealone_albums():
    sql = '''
    SELECT Title, ID, Path
    FROM Album 
        '''
    conn, c = connect()
    items = []
    try:
        items = c.execute(sql).fetchall()
    except:
        print_error(sql, 'apeflac')
    conn.close()
    out = []
    for item in items:
        pieces = get_pieces(item[1])
        count_ape = 0
        count_flac = 0
        count_cue = 0
        count_piece = 0
        for piece in pieces:
            ext = get_extension(piece['Name'])
            if ext == 'flac':
                count_flac += 1
            if ext == 'ape':
                count_ape += 1
            if ext == 'cue':
                count_cue += 1
            else:
                count_piece += 1
        if count_ape > 0 and count_flac == 0:
        # if 3 > count_ape > 0 == count_flac \
        #         and count_cue == 1:
            it = {
                'Title': item[0],
                'ID': item[1],
                'Path': item[2],
                'CountApe': count_ape,
                'CountFlac': count_flac,
                'CountCues': count_cue,
                'CountPieces': count_piece
            }
            out.append(it)
    return out


# def get_missing_score():
#     sql = '''
#     select DISTINCT LibraryCode from Piece
#     where LibraryCode like 'K %'
#     order by length(LibraryCode), LibraryCode
#     '''
#     conn, c = connect()
#     items = []
#     try:
#         items = c.execute(sql).fetchall()
#     except:
#         print('in db encoding error')
#     conn.close()
#     out = []
#     for item in items:
#         image_path = SCORE_FRAGMENT_PATH.format(item[0])
#         if not os.path.exists(image_path):
#             out.append(item)
#     return out


def get_widow_albums():
    """
    albums zonder stukken erin en tegelijk ook geen albums die erin zitten
    :return:
    """
    sql = '''
SELECT A1.Title, A1.ID, A1.Path
FROM Album A1
  LEFT JOIN Piece ON Piece.AlbumID = A1.ID
  LEFT JOIN Album A2 ON A2.AlbumID = A1.ID
WHERE Piece.Name ISNULL
AND A2.AlbumID ISNULL
ORDER BY A1.Title COLLATE NOCASE
    '''
    conn, c = connect()
    items = []
    try:
        items = c.execute(sql).fetchall()
    except:
        print_error(sql, 'get_widow_albums')
    conn.close()
    out = []
    # delete_not_existing_path_albums(items)
    for item in items:
        it = {
                'Title': item[0],
                'ID': item[1],
                'Path': item[2],
            }
        doubles = get_path_doubles(it)
        if len(doubles) == 0:
            out.append(it)
        # else:
        #     print it['Title'], ' has doubles'
    return out


sql_librarycode_old = '''
  SELECT Code, Tempo, Key, Alias
   FROM LibraryCode
   WHERE LibraryCode.Code LIKE ?
   ORDER BY length(Code), Code
  '''


# split Code in Code1 and Code2 for sorting properly
# e.g. 'BWV 1020_3' becomes 'BWV 1020' and '3'
# placeholder would be k_wild
sql_librarycode = '''
SELECT
  Code,
  Code1,
  Code2,
  Tempo,
  Key,
  Alias,
  Title,
  Favorite
FROM (
  SELECT
    Code,
    CASE WHEN ic > 0
      THEN Code1
    ELSE Code2 END AS Code1,
    CASE WHEN ic > 0
      THEN Code2
    ELSE NULL END  AS Code2,
    Tempo,
    Key,
    Alias,
    Title,
    Favorite
  FROM
    (SELECT
       ic,
       Code,
       substr(Code, 0, ic) Code1,
       substr(Code, ic)    Code2,
       Tempo,
       Key,
       Alias,
       Title,
       Favorite
     FROM
       (SELECT
          instr(Code, '_') ic,
          Code,
          Tempo,
          Key,
          Alias,
          Title,
          Favorite
        FROM LibraryCode
        WHERE LibraryCode.Code LIKE ?
        {}
       )
    )
)
ORDER BY length(Code1), Code1, Code2
'''


# split Code in Code1 and Code2 for sorting properly
# place numeric part of Code1 in Code0 (for comparison with range)
# e.g. 'BWV 1020_3' becomes:
# Code1: 'BWV 1020'
# Code2: '3'
# Code0: 1020
# placeholders would be k_wild, min, max
sql_librarycode_range = '''
SELECT
  Code,
  Code0,
  Code1,
  Code2,
  Tempo,
  Key,
  Alias,
  Title,
  Favorite
FROM (
SELECT
  Code,
  CAST(substr(Code1, instr(Code1, ' ')) AS INT) Code0,
  Code1,
  Code2,
  Tempo,
  Key,
  Alias,
  Title,
  Favorite
FROM (
  SELECT
    Code,
    CASE WHEN ic > 0
      THEN Code1
    ELSE Code2 END AS Code1,
    CASE WHEN ic > 0
      THEN Code2
    ELSE NULL END  AS Code2,
    Tempo,
    Key,
    Alias,
    Title,
    Favorite
  FROM
    (SELECT
       ic,
       Code,
       substr(Code, 0, ic) Code1,
       substr(Code, ic)    Code2,
       Tempo,
       Key,
       Alias,
       Title,
       Favorite
     FROM
       (SELECT
          instr(Code, '_') ic,
          Code,
          Tempo,
          Key,
          Alias,
          Title,
          Favorite
        FROM LibraryCode
        WHERE LibraryCode.Code LIKE ?
        {}
       )
    )
))
WHERE Code0 >= ? AND Code0 <= ?
ORDER BY length(Code1), Code1, Code2;
'''


def get_librarycode(code):
    sql = '''
      SELECT Code, Tempo, Key, Alias, Title, Favorite
       FROM LibraryCode
       WHERE LibraryCode.Code=?
       ORDER BY length(Code), Code
      '''
    item = get_item_with_id(sql, code)
    if not item or not len(item):
        return None
    out = item
    return {
        'Code': out[0],
        'Tempo': out[1],
        'Key': out[2],
        'Alias': out[3],
        'Title': out[4],
        'Favorite': out[5],
    }


def get_librarycode_sonatas_range(k_wild, min, max, favorite=None):
    if favorite:
        sql = sql_librarycode_range.format('AND Favorite=?')
        params = (k_wild, min, max, favorite, )
    else:
        sql = sql_librarycode_range.format('')
        params = (k_wild, min, max,)
    items = execute(sql, params)
    out = []
    for item in items:
        out.append({
            'k_code': item[0],
            'code1': item[2],
            'code2': item[3],
            'Tempo': item[4],
            'Key': item[5],
            'Alias': item[6],
            'Title': item[7],
            'Favorite': item[8],
        })
    return out


def get_librarycode_sonatas(k_wild, favorite=None):
    if favorite:
        sql = sql_librarycode.format('AND Favorite=?')
        params = (k_wild, favorite, )
    else:
        sql = sql_librarycode.format('')
        params = (k_wild, )

    items = execute(sql, params)
    out = []
    for item in items:
        out.append({
            'k_code': item[0],
            'code1': item[1],
            'code2': item[2],
            'Tempo': item[3],
            'Key': item[4],
            'Alias': item[5],
            'Title': item[6],
            'Favorite': item[7],
        })
    return out


def get_librarycode_explanation(code, range=None):
    conn, c = connect()
    if range:
        sql = '''
        SELECT Explanation, ComponistID
        FROM Librarycode_Explanation
        WHERE LibraryCode=?
        AND Range=?
        '''
        return c.execute(sql, (code, range, )).fetchone()
    else:
        sql = '''
        SELECT Explanation, ComponistID
        FROM Librarycode_Explanation
        WHERE LibraryCode=?
        '''
        return c.execute(sql, (code, )).fetchone()


def get_pianoboek_nummers(boek_id):
    sql = '''
    SELECT 
      L.Code,
      LP.Nr,
      L.Tempo,
      L.Key
     FROM LibraryCode L
     JOIN LibraryCode_Pianoboek LP
     ON L.Code=LP.LibraryCode
     WHERE LP.PianoboekID=?
     ORDER BY length(LP.Nr), LP.Nr
    '''
    items = get_items_with_parameter(sql, boek_id)
    out = []
    for item in items:
        out.append({
            'Code': item[0],
            'Nr': item[1],
            'Tempo': item[2],
            'Key': item[3],
        })
    return out


def get_pianoboek(boek_id):
    sql = '''
    SELECT 
    P.Name, 
    P.Nr, 
    P.ID, 
    U.Name,
    C.FirstName,
    C.LastName
    FROM Pianoboek P
    JOIN Uitgever U
    ON U.ID = P.UitgeverID
    JOIN Componist C
    ON C.ID = P.ComponistID
    WHERE P.ID = ?
    '''
    items = get_items_with_parameter(sql, boek_id)
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'Nr': item[1],
            'ID': item[2],
            'Uitgever': item[3],
            'Componist': item[4] + ' ' + item[5]
        })
    return out[0]


def get_pianoboeken():
    sql = '''
    SELECT 
    P.Name, 
    P.Nr, 
    P.ID, 
    U.Name,
    C.FirstName,
    C.LastName
    FROM Pianoboek P
    JOIN Uitgever U
    ON U.ID = P.UitgeverID
    JOIN Componist C
    ON C.ID = P.ComponistID
    '''
    items = get_items(sql)
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'Nr': item[1],
            'ID': item[2],
            'Uitgever': item[3],
            'Componist': item[4] + ' ' + item[5]
        })
    return out


def get_librarycode_boek(k_code):
    sql = '''
      SELECT 
        Pianoboek.Name, 
        LibraryCode_Pianoboek.Nr,
        Uitgever.Name,
        Pianoboek.ID
      FROM LibraryCode_Pianoboek
      JOIN Pianoboek
      ON Pianoboek.ID = LibraryCode_Pianoboek.PianoboekID
      JOIN Uitgever
      ON Uitgever.ID=Pianoboek.UitgeverID
      WHERE LibraryCode_Pianoboek.LibraryCode=?
      '''
    items = get_items_with_parameter(sql, k_code)
    out = []
    for item in items:
        out.append({
            'Name': item[0],
            'Nr': item[1],
            'Uitgever': item[2],
            'ID': item[3]
        })
    return out


def get_librarycode_sonata(k_code, instrument_id=None):
    sql = '''
      SELECT 
        Piece.ID,
        Piece.Name,
        Instrument.Name,
        Instrument.ID,
        Album.Title,
        Album.ID
       FROM Piece
       JOIN Album
       ON Piece.AlbumID = Album.ID
       LEFT JOIN Instrument
       ON Album.InstrumentID = Instrument.ID
          WHERE Piece.LibraryCode=?
          '''
    if instrument_id:
        sql += 'AND Instrument.ID=?'
    sql += '''
      ORDER BY Instrument.Name
      '''

    if instrument_id:
        items = get_items_with_2parameter(sql, k_code, instrument_id)
    else:
        items = get_items_with_parameter(sql, k_code)
    out = []
    for item in items:
        out.append({
            'Piece': {
                'Name': item[1],
                'ID': item[0],
            },
            'Instrument': {
                'Name': item[2],
                'ID': item[3],
            },
            'Album': {
                'Title': item[4],
                'ID': item[5],
            }
        })
    return out


def get_bach_k_pieces():
    return get_k_pieces('gold %')


def get_scarlatti_k_pieces():
    return get_k_pieces('K %')


def get_k_pieces(k_wild):
    sql = '''
      SELECT 
        Piece.LibraryCode, 
        Piece.Name, 
        Piece.ID,
        Performer.FirstName, 
        Performer.LastName, 
        Performer.ID, 
        Instrument.Name,
        Instrument.ID,
        Album.Title,
        Album.ID
      FROM Piece
       JOIN Album
       ON Piece.AlbumID = Album.ID
       JOIN Performer_Album
       ON Performer_Album.AlbumID = Album.ID
       JOIN Performer
       ON Performer_Album.PerformerID = Performer.ID
       JOIN Instrument
       ON Album.InstrumentID = Instrument.ID
      WHERE LibraryCode LIKE ?
      ORDER BY LENGTH(LibraryCode), LibraryCode
    '''
    items = get_items_with_parameter(sql, k_wild)
    out = []
    for item in items:
        out.append({
            'k_code': item[0],
            'Piece': {
                'Name': item[1],
                'ID': item[2],
            },
            'Artiest': {
                'Name': u'{} {}'.format(item[3], item[4]),
                'ID': item[5],
            },
            'Instrument': {
                'Name': item[6],
                'ID': item[7],
            },
            'Album': {
                'Title': item[8],
                'ID': item[9],
            }
        })
    return out


def get_tag(id_tag):
    sql = '''
    SELECT Name, ID 
    FROM Tag WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_tag)
    return {
        "Name": fields[0],
        "ID": fields[1],
    }


def get_performer(id_performer):
    sql = '''
    SELECT FirstName, LastName, Birth, Death, Path, ID 
    FROM Performer WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_performer)
    return {
        "FirstName": fields[0],
        "LastName": fields[1],
        "FullName": make_fullname(fields[0], fields[1]),
        "Birth": fields[2],
        "Death": fields[3],
        "Path": fields[4],
        "ID": fields[5],
    }


def get_cuesheet(cuesheet_id, c):
    sql = '''
    SELECT P.Name, A.Path
    FROM Piece P
    JOIN Album A ON P.AlbumID = A.ID
    WHERE P.ID=?
    '''
    fields = c.execute(sql, (cuesheet_id,)).fetchone()
    return {
        'Name': fields[0],
        'AlbumPath': fields[1],
    }


def get_album_by_id(album_id):
    sql = '''
    SELECT Title, ID 
    FROM Album 
    WHERE Album.ID=?
    '''
    c, conn = connect()
    fields = c.execute(sql, (album_id,)).fetchone()
    if not fields:
        print('ID not found')
        return None
    return {
        'Title': fields[0],
        'ID': fields[1]
    }


def get_album_path_by_id(album_id, c):
    sql = '''
    SELECT Path 
    FROM Album 
    WHERE Album.ID=?
    '''
    fields = c.execute(sql, (album_id,)).fetchone()
    if not fields:
        print('ID not found')
        return None
    return fields[0]


def get_componist_path_by_id(componist_id, c):
    sql = '''
    SELECT Path 
    FROM Componist 
    WHERE ID=?
    '''
    fields = c.execute(sql, (componist_id,)).fetchone()
    return fields[0]


def get_componist_id_from_album(album_id, c):
    sql = '''
    SELECT ComponistID 
    FROM Componist_Album 
    WHERE AlbumID=?
    '''
    fields = c.execute(sql, (album_id,)).fetchone()
    return fields[0]


def get_album(id_album):
    sql = '''
    SELECT Title, Label, Path, AlbumID, Description, ID 
    FROM Album
    WHERE Album.ID=?
    '''
    fields = get_item_with_id(sql, id_album)
    if not fields:
        print(id_album)
        print('has no items')
        return {}
    return {
        "Title": fields[0],
        "Label": fields[1],
        "Path": fields[2],
        "AlbumID": fields[3],
        "Description": fields[4],
        "ID": fields[5],
    }


def get_componist_path_c(componist_id, c):
    sql = '''
    SELECT Path
    FROM Componist
    WHERE ID=?
    '''
    fields = c.execute(sql, (componist_id,)).fetchone()
    return fields[0]


def get_element(album_id, name, c):
    sql = None
    if name == 'instrument':
        sql = '''
        SELECT Name, ID
        FROM Instrument
        WHERE ID in (
          SELECT InstrumentID
          FROM Album
          WHERE Album.ID = ?
        )
        '''
        fields = c.execute(sql, (album_id,)).fetchone()
        if fields:
            return fields[0] + '_' + str(fields[1])
        return None
    if name == 'componist':
        sql = '''
        SELECT LastName, Componist.ID
        FROM Componist
        LEFT JOIN Componist_Album
        ON ComponistID=Componist.ID
        WHERE AlbumID=?
        '''
    if name == 'performer':
        sql = '''
        SELECT LastName, Performer.ID
        FROM Performer
        LEFT JOIN Performer_Album
        ON PerformerID=Performer.ID
        WHERE AlbumID=?
        '''
    if name == 'tag':
        sql = '''
        SELECT Name, Tag.ID
        FROM Tag
        LEFT JOIN Tag_Album
        ON TagID=Tag.ID
        WHERE AlbumID=?
        '''
    if sql:
        fields = c.execute(sql, (album_id,)).fetchone()
        return fields[0] + '_' + str(fields[1])
    return None


def get_album_by_path(path, c):
    sql = '''
    SELECT Title, Label, Path, AlbumID, ID 
    FROM Album 
    WHERE Album.Path=?
    '''
    fields = c.execute(sql, (path,)).fetchone()
    if not fields:
        # print(path)
        # print('has no items')
        return None
    return {
        "Title": fields[0],
        "Label": fields[1],
        "Path": fields[2],
        "AlbumID": fields[3],
        "ID": fields[4],
    }


def get_album_id_by_path(path, c, conn):
    sql = '''
    SELECT ID 
    FROM Album 
    WHERE Album.Path=?
    '''
    fields = c.execute(sql, (path,)).fetchone()
    if not fields:
        return None
    return fields[0]


def get_mother_title(id_album):
    sql = '''
    SELECT Title 
    FROM Album 
    WHERE Album.ID=?
    '''
    fields = get_item_with_id(sql, id_album)
    if not fields:
        return None
    return fields[0]


def get_piece(id_piece):
    sql = '''
    SELECT Name, AlbumID, ID, NPlayed FROM Piece WHERE ID=?
    '''
    fields = get_item_with_id(sql, id_piece)
    return {
        "Name": fields[0],
        "AlbumID": fields[1],
        "ID": fields[2],
        "NPlayed": fields[3],
    }


def get_album_by_title(title, c, conn):
    sql = '''
    SELECT COUNT(ID) FROM Album
     WHERE Title=?
    '''
    fields = c.execute(sql, (title,)).fetchone()
    return {
        "Count": fields[0],
    }


def get_album_count_by_path(path, c, conn):
    sql = '''
    SELECT COUNT(ID) FROM Album
     WHERE Path=?
    '''
    fields = c.execute(sql, (path,)).fetchone()
    return {
        "Count": fields[0],
    }


def get_albums_ncreated(n):
    sql = '''
    SELECT ID, Title, Created
    FROM Album
    ORDER BY Created DESC
    LIMIT ?
    '''
    con, c = connect()
    items = c.execute(sql, (int(n), )).fetchall()
    out = []
    for fields in items:
        # 2018-02-06 09:02:57
        # 2018-02-06 09:02:57
        ftime = '%Y-%m-%d %H:%M:%S'
        dt = None
        if fields[2]:
            dt = datetime.strptime(fields[2], ftime)
        out.append({
            'ID': fields[0],
            'Title': fields[1],
            'Created': dt,
        })
    return out


def get_pieces_nplayed(n):
    sql = '''
    SELECT P.ID, Name, NPlayed, LastPlayed, A.ID, A.Title
    FROM Piece P
    JOIN Album A ON P.AlbumID = A.ID
    WHERE NPlayed > 0
    ORDER BY LastPlayed DESC
    LIMIT ?
    '''
    con, c = connect()
    items = c.execute(sql, (int(n), )).fetchall()
    out = []
    for fields in items:
        # 2018-02-06 09:02:57
        ftime = '%Y-%m-%d %H:%M:%S'
        ftimed = '%Y-%m-%d'
        dt = None
        if fields[3]:
            if len(fields[3]) > 10:
                dt = datetime.strptime(fields[3], ftime)
            else:
                dt = datetime.strptime(fields[3], ftimed)
        out.append( {
            'Piece': {
                'ID': fields[0],
                'Name': fields[1],
                "NPlayed": fields[2],
                'LastPlayed': dt,
            },
            'Album': {
                'ID': fields[4],
                'Title': fields[5],
            },
        })
    return out
