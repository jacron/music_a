from website.db.fetch import (get_pieces, get_album_albums,
                              get_album_componisten, get_album_performers,
                              get_album_instruments, get_album,
                              get_piece, )
from website.db.insert import (
    insert_album_componist, insert_album_performer,
    insert_album_instrument, insert_album, )
from website.db.pieces import insert_pieces
from website.lib.color import ColorPrint
from music.settings import SKIP_DIRS, AUDIO_ROOT
from website.scripts.helper.socket import socket_log
from website.services.services import splits_naam, splits_years, get_extension
from .connect import connect
import os


def get_library_code(name):
    parts = name.split('K. ')
    if len(parts) < 2:
        parts = name.split('K.')
    if len(parts) < 2:
        parts = name.split('KK.')
    if len(parts) < 2:
        parts = name.split('K ')
    if len(parts) < 2:
        return None
    kk = parts[1].split(' ')
    if len(kk) < 2:
        kk = parts[1].split('.')
    if len(kk) < 2:
        kk = parts[1].split(',')
    return 'K ' + kk[0]


def adjust_kk(album_id):
    pieces = get_pieces(album_id)
    for piece in pieces:
        library_code = get_library_code(piece[0])
        if library_code:
            update_piece_library_code(piece[1], library_code)


def inherit_album(album, componisten, performers, instrument, c, conn):
    for componist in componisten:
        insert_album_componist(componist['ID'], album['ID'], c, conn)
    for performer in performers:
        insert_album_performer(performer['ID'], album['ID'], c, conn)
    if instrument:
        insert_album_instrument(instrument['ID'], album['ID'], c, conn)


def inherit_elements(album_id):
    albums = get_album_albums(album_id)
    componisten = get_album_componisten(album_id)
    performers = get_album_performers(album_id)
    instrument = get_album_instruments(album_id)
    conn, c = connect()
    for album in albums:
        inherit_album(album, componisten, performers, instrument, c, conn)


def update_librarycode(code, favorite):
    sql = '''
    UPDATE LibraryCode
    SET Favorite=?
    WHERE Code=?'''
    con, c = connect()
    c.execute(sql, (favorite, code,)).fetchone()
    con.commit()


def update_librarycode_title(code, text):
    sql = '''
    UPDATE LibraryCode
    SET Title=?
    WHERE Code=?'''
    con, c = connect()
    c.execute(sql, (text, code,)).fetchone()
    con.commit()
    return text


def update_librarycode_alias(code, text):
    sql = '''
    UPDATE LibraryCode
    SET Alias=?
    WHERE Code=?'''
    con, c = connect()
    c.execute(sql, (text, code,)).fetchone()
    con.commit()
    return text


def update_piece_library_code(piece_id, code):
    sql = '''
    UPDATE Piece
    SET LibraryCode=?
    WHERE ID=?
    '''
    con, c = connect()
    c.execute(sql, (code, piece_id,)).fetchone()
    con.commit()
    sql = '''
    INSERT OR IGNORE 
    INTO LibraryCode
    (Code)
    VALUES(?)
    '''
    con, c = connect()
    c.execute(sql, (code,)).fetchone()
    con.commit()


def update_album_title(album_id, title):
    sql = """
    UPDATE Album 
    SET Title=?
    WHERE Album.ID=?
    """
    con, c = connect()
    c.execute(sql, (title, album_id,)).fetchone()
    con.commit()
    return 'Album title updated to: ' + title


def update_db_piece_name(piece_id, piece_name):
    sql = """
    UPDATE Piece 
    SET Name=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (piece_name, piece_id,)).fetchone()
    con.commit()


def update_album_description(album_id, description):
    sql = """
    UPDATE Album 
    SET Description=?
    WHERE Album.ID=?
    """
    con, c = connect()
    c.execute(sql, (description, album_id,)).fetchone()
    con.commit()


def add_new_componist_to_album(name, albumid):
    # name is not unambivalently translatable in firstname and lastname
    # so we search for it existing first
    sql = """
    SELECT ID FROM Componist
    WHERE FirstName || ' ' || LastName=?
    """
    con, c = connect()
    componist_id = c.execute(sql, (name,)).fetchone()
    con.close()
    if not componist_id:
        componist_id = new_componist(name)
    if componist_id:
        add_componist_to_album(componist_id[0], albumid)


def add_new_performer_to_album(name, albumid):
    # name is not unambivalently translatable in firstname and lastname
    # so we search for it existing first
    sql = """
    SELECT ID FROM Performer
    WHERE FirstName || ' ' || LastName=?
    """
    con, c = connect()
    performer_id = c.execute(sql, (name,)).fetchone()
    con.close()
    if not performer_id:
        performer_id = new_performer(name)
    if performer_id:
        add_performer_to_album(performer_id[0], albumid)


def add_componist_to_album(componistid, albumid):
    sql = """
    INSERT OR IGNORE INTO Componist_Album 
    (ComponistID, AlbumID)
    VALUES(?,?)
    """
    con, c = connect()
    c.execute(sql, (componistid, albumid,)).fetchone()
    con.commit()
    return 'componist {} added to album {}'.format(componistid, albumid)


def add_performer_to_album(performerid, albumid):
    sql = """
    INSERT OR IGNORE INTO Performer_Album 
    (PerformerID, AlbumID)
    VALUES(?,?)
    """
    con, c = connect()
    c.execute(sql, (performerid, albumid,)).fetchone()
    con.commit()
    return 'performer {} added to album {}'.format(performerid, albumid)


def add_tag_to_album(tagid, albumid):
    sql = """
    INSERT OR IGNORE INTO Tag_Album 
    (TagID, AlbumID)
    VALUES(?,?)
    """
    con, c = connect()
    c.execute(sql, (tagid, albumid,)).fetchone()
    con.commit()
    return 'tag {} added to album {}'.format(tagid, albumid)


def delete_piece(piece_id):
    sql = '''
    DELETE FROM Piece
    WHERE ID=?
    '''
    con, c = connect()
    c.execute(sql, (piece_id,))
    con.commit()


# def delete_piece(piece_id):
#     sql = """
#     DELETE FROM Piece
#      WHERE ID=?
#     """
#     con, c = connect()
#     c.execute(sql, (piece_id,)).fetchone()
#     con.commit()


def remove_piece(album_id, piece_name):
    album = get_album(album_id)
    p = os.path.join(album['Path'], piece_name)
    try:
        os.remove(p)
    except FileNotFoundError as ex:
        ColorPrint.print_c(str(ex), ColorPrint.CYAN)
        socket_log(str(ex), 'error', album_id)
    except PermissionError as p:
        ColorPrint.print_c(str(p), ColorPrint.CYAN)
        socket_log(str(p), 'error', album_id)


def delete_album_ape(album_id):
    pieces = get_pieces(album_id)
    for piece in pieces:
        if get_extension(piece['Name']) == 'ape':
            remove_piece(album_id, piece['Name'])
            delete_piece(piece['ID'])
            socket_log(msg=piece['Name'] + ' deleted', mode='info', id=album_id)


def remove_tag_from_album(tagid, albumid):
    sql = """
    DELETE FROM Tag_Album
     WHERE TagID=? AND AlbumID=?
    """
    con, c = connect()
    c.execute(sql, (tagid, albumid,)).fetchone()
    con.commit()
    return 'tag {} removed from album {}'.format(tagid, albumid)


def update_tag_name(tag_id, name):
    sql = """
    UPDATE Tag
    SET Name=? 
     WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (name, tag_id,)).fetchone()
    con.commit()
    return 'Tag {} name changed to {}'.format(tag_id, name)


def remove_componist_from_album(componist_id, albumid):
    sql = """
    DELETE FROM Componist_Album
     WHERE ComponistID=? AND AlbumID=?
    """
    con, c = connect()
    c.execute(sql, (componist_id, albumid,)).fetchone()
    con.commit()
    return 'componist {} removed from album {}'.format(componist_id, albumid)


def remove_performer_from_album(performer_id, albumid):
    sql = """
    DELETE FROM Performer_Album
     WHERE PerformerID=? AND AlbumID=?
    """
    con, c = connect()
    c.execute(sql, (performer_id, albumid,)).fetchone()
    con.commit()
    return 'performer {} removed from album {}'.format(performer_id, albumid)


def remove_instrument_from_album(albumid):
    if not albumid:
        print('error')
        return
    sql = """
    UPDATE Album
    SET InstrumentID=NULL 
     WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (albumid,)).fetchone()
    con.commit()


def add_instrument_to_album(instrumentid, albumid):
    sql = """
    UPDATE Album
    SET InstrumentID=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (instrumentid, albumid,)).fetchone()
    con.commit()


def add_new_instrument_to_album(name, albumid):
    print(albumid)
    sql = '''
    SELECT ID FROM Instrument WHERE Name=?
    '''
    con, c = connect()
    instrument_id = c.execute(sql, (name,)).fetchone()
    con.close()
    print(instrument_id)
    if not instrument_id:
        instrument_id = new_instrument(name)
    if instrument_id:
        add_instrument_to_album(instrument_id[0], albumid)


def new_componist(name):
    c_firstname, c_lastname = splits_naam(name)
    sql = """
    INSERT OR IGNORE INTO Componist 
    (FirstName, LastName)
    VALUES(?,?)
    """
    con, c = connect()
    c.execute(sql, (c_firstname, c_lastname,)).fetchone()
    con.commit()
    sql = '''
    SELECT ID FROM Componist WHERE FirstName=? AND LastName=?
    '''
    return c.execute(sql, (c_firstname, c_lastname,)).fetchone()


def new_performer(name):
    c_firstname, c_lastname = splits_naam(name)
    sql = """
    INSERT OR IGNORE INTO Performer 
    (FirstName, LastName)
    VALUES(?,?)
    """
    con, c = connect()
    c.execute(sql, (c_firstname, c_lastname,)).fetchone()
    con.commit()
    sql = '''
    SELECT ID FROM Performer WHERE FirstName=? AND LastName=?
    '''
    return c.execute(sql, (c_firstname, c_lastname,)).fetchone()


def new_tag(name):
    sql = """
    INSERT OR IGNORE INTO Tag 
    (Name)
    VALUES(?)
    """
    con, c = connect()
    c.execute(sql, (name,)).fetchone()
    con.commit()
    sql = '''
    SELECT ID FROM Tag WHERE Name=?
    '''
    return c.execute(sql, (name,)).fetchone()


def new_instrument(name):
    sql = """
    INSERT OR IGNORE INTO Instrument 
    (Name)
    VALUES(?)
    """
    con, c = connect()
    c.execute(sql, (name,)).fetchone()
    con.commit()
    sql = '''
    SELECT ID FROM Instrument WHERE Name=?
    '''
    return c.execute(sql, (name,)).fetchone()


def update_componistname(name, componist_id):
    first_name, last_name = splits_naam(name)
    sql = """
    UPDATE Componist
    SET FirstName=?, LastName=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (first_name, last_name, componist_id,)).fetchone()
    con.commit()
    return 'name for person {} changed to {}'.format(componist_id, name)


def update_componistyears(years, componist_id):
    birth, death = splits_years(years)
    sql = """
    UPDATE Componist
    SET Birth=?, Death=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (birth, death, componist_id,)).fetchone()
    con.commit()
    return 'years for person {} changed to {}'.format(componist_id, years)


def update_componistbirth(years, componist_id):
    sql = """
    UPDATE Componist
    SET Birth=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (years, componist_id,)).fetchone()
    con.commit()
    return 'year of birth for person {} changed to {}'.format(componist_id,
                                                              years)


def update_componistdeath(years, componist_id):
    sql = """
    UPDATE Componist
    SET Death=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (years, componist_id,)).fetchone()
    con.commit()
    return 'year of death for person {} changed to {}'.format(componist_id,
                                                              years)


def update_componistrole(text, componist_id):
    sql = """
    UPDATE Componist
    SET Role=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (text, componist_id,)).fetchone()
    con.commit()
    return 'role for person {} changed to {}'.format(componist_id, text)


def update_performerbirth(years, person_id):
    sql = """
    UPDATE Performer
    SET Birth=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (years, person_id,)).fetchone()
    con.commit()
    return 'yearof birth for person {} changed to {}'.format(person_id, years)


def update_performerdeath(years, person_id):
    sql = """
    UPDATE Performer
    SET Death=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (years, person_id,)).fetchone()
    con.commit()
    return 'year of death for person {} changed to {}'.format(person_id, years)


def update_performername(name, performer_id):
    first_name, last_name = splits_naam(name)
    sql = """
    UPDATE Performer
    SET FirstName=?, LastName=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (first_name, last_name, performer_id,)).fetchone()
    con.commit()
    return 'name for person {} changed to {}'.format(performer_id, name)


def update_performerrole(text, performer_id):
    sql = """
    UPDATE Performer
    SET Role=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (text, performer_id,)).fetchone()
    con.commit()
    return 'role for person {} changed to {}'.format(performer_id, text)


def delete_pieces_of_album(album_id):
    sql = '''
    DELETE FROM Piece
    WHERE AlbumID=?
    '''
    con, c = connect()
    c.execute(sql, (album_id,)).fetchone()
    con.commit()


def delete_tag(tag_id):
    sql = """
    DELETE FROM Tag
    WHERE ID=?"""
    con, c = connect()
    c.execute(sql, (tag_id,)).fetchone()
    con.commit()


def delete_performer(performer_id):
    sql = """
    DELETE FROM Performer
    WHERE ID=?"""
    con, c = connect()
    c.execute(sql, (performer_id,)).fetchone()
    con.commit()
    sql = """
    DELETE FROM Performer_Album
    WHERE PerformerID=?"""
    con, c = connect()
    c.execute(sql, (performer_id,)).fetchone()
    con.commit()


def delete_componist(componist_id):
    sql = """
    DELETE FROM Componist
    WHERE ID=?"""
    con, c = connect()
    c.execute(sql, (componist_id,)).fetchone()
    con.commit()
    sql = """
    DELETE FROM Componist_Album
    WHERE ComponistID=?"""
    con, c = connect()
    c.execute(sql, (componist_id,)).fetchone()
    con.commit()


def delete_instrument(instrument_id):
    sql = """
    DELETE FROM Instrument
    WHERE ID=?"""
    con, c = connect()
    c.execute(sql, (instrument_id,)).fetchone()
    con.commit()


def delete_album(album_id):
    sql = """
    DELETE FROM Album
    WHERE ID=?"""
    con, c = connect()
    c.execute(sql, (album_id,)).fetchone()
    con.commit()
    sql = """
    DELETE FROM Componist_Album
    WHERE AlbumID=?"""
    con, c = connect()
    c.execute(sql, (album_id,)).fetchone()
    con.commit()


def process_album(path, mother_id):
    """
    haal stukken (cuesheets en music files) op voor een album
    """
    conn, c = connect()
    w = path.split('/')
    album_title = w[-1].replace("_", " ")
    dbpath = path.replace(AUDIO_ROOT, '')

    album_id = insert_album(
        title=album_title,
        path=dbpath,
        is_collectie=0,
        c=c,
        conn=conn,
        album_id=mother_id,
    )[0]
    ColorPrint.print_c("album_id={}".format(album_id), ColorPrint.LIGHTCYAN)
    insert_pieces(path, album_id, conn, c)
    conn.close()
    return album_id


def read_albums(album_id):
    album = get_album(album_id)
    # get_albums(album['Path'], None, 0)
    path = os.path.join(AUDIO_ROOT, album['Path'])
    for d in os.listdir(path):
        p = u'{}/{}'.format(path, d)
        if os.path.isdir(p) and d not in SKIP_DIRS:
            process_album(p, album_id)


def update_performeryears(years, performer_id):
    birth, death = splits_years(years)
    sql = """
    UPDATE Performer
    SET Birth=?, Death=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (birth, death, performer_id,)).fetchone()
    con.commit()


def add_path_to_componist(componist_id, path):
    sql = """
    UPDATE Componist
    SET Path=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (path, componist_id,)).fetchone()
    con.commit()


def add_path_to_performer(performer_id, path):
    sql = """
    UPDATE Performer
    SET Path=?
    WHERE ID=?
    """
    con, c = connect()
    c.execute(sql, (path, performer_id,)).fetchone()
    con.commit()


def set_album_title(album_id, title, c, con):
    sql = """
    UPDATE Album 
    SET TITLE=? 
    WHERE ID=?
    """
    c.execute(sql, (title, album_id,)).fetchone()
    con.commit()


def update_played(piece_id):
    piece = get_piece(piece_id)
    n_played = piece['NPlayed']
    if not n_played:
        n_played = 0
    n_played += 1
    sql = '''
    UPDATE Piece
    SET NPlayed=?, LastPlayed=DateTime('now')
    WHERE ID=?
    '''
    con, c = connect()
    c.execute(sql, (n_played, piece_id,)).fetchone()
    con.commit()


def toggle_setting(name):
    sql = """
    UPDATE Settings
    SET VALUE = NOT VALUE 
    WHERE Name=?
    """
    con, c = connect()
    c.execute(sql, (name,)).fetchone()
    con.commit()
