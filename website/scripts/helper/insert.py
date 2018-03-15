from website.db.insert import insert_performer, insert_album_performer, \
    insert_album_componist, insert_componist

# k_split = None


def kirkpatrick(filepath, k_split='K ', end_limit=' '):
    if k_split:
        w = filepath.split('/')
        name = w[-1]
        k = name.split(k_split)
        if len(k) > 1:
            return 'K ' + k[1].split(end_limit)[0]
    return 0


def filename(filepath):
    name = filepath.split('/')[-1]
    return name  # .replace("_", " ")


def insert_artiest(artiest, c, conn, album_id):
    if artiest:
        performer_id = insert_performer(artiest, c, conn)[0]
    else:
        performer_id = None
    if performer_id:
        insert_album_performer(performer_id, album_id, c, conn)


def insert_componist_by_id(cid, c, conn, album_id):
    insert_album_componist(cid, album_id, c, conn)


def insert_performer_by_id(cid, c, conn, album_id):
    insert_album_performer(cid, album_id, c, conn)


def insert_composer(componist, c, conn, album_id):
    if componist:
        componist_id = insert_componist(componist, c, conn)[0]
    else:
        componist_id = None
    if componist_id:
        insert_album_componist(componist_id, album_id, c, conn)
