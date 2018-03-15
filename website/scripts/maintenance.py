from __future__ import unicode_literals

import sqlite3

# from website.db import delete_album_completely
from db.insert import delete_album_completely

db_path = '../../db.sqlite3'


def delete_albums(ids):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for aid in ids:
        delete_album_completely(aid, c, conn)
        print('removed id:{}'.format(aid))


def get_library_code(part):
    name_part = part[4:]
    nn = name_part.split(' ')
    if len(nn) < 2:
        nn = name_part.split(']')
    if len(nn) < 2:
        nn = name_part.split(',')
    if len(nn) < 2:
        nn = name_part.split('.')
    return 'BWV ' + nn[0]


def write_bwv():
    sql = '''
    SELECT Name, substr(Name, instr(Name, 'BWV')) name_part, ID
    FROM Piece
    WHERE Name LIKE '%BWV%'
    ORDER BY name_part
    '''
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    items = c.execute(sql, ).fetchall()
    for item in items:
        library_code = get_library_code(item[1])
        print(item[0], library_code)



def main():
    # delete_albums([5087, 5086, 5088, ])
    write_bwv()

if __name__ == '__main__':
    main()
