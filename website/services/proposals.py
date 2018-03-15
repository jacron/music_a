# from unidecode import unidecode
# from ..db import (
#     get_componisten, get_performers,
#     get_componist, get_componist_aliasses, get_performer_aliasses,
# get_performer, )
from ..db.fetch import get_componist, get_performer, get_componisten, \
    get_componist_aliasses, get_performers, get_performer_aliasses


def has_alias(s, persons, id_field):
    proposals = []
    if s is None:
        return []
    s = s.replace('_', ' ')
    # try:
    #     s = unidecode(s.upper())
    # except Exception:
    s = s.upper()
    for person in persons:
        # p = unidecode(person['Name'].upper())
        p = person['Name'].upper()
        if len(p) > 2 and person.get(id_field) and p in s:
            if id_field == 'ComponistID':
                fperson = get_componist(person.get(id_field))
            else:
                fperson = get_performer(person.get(id_field))
            proposals.append(fperson)
    return proposals


def has_person(s, persons):
    proposals = []
    if s is None:
        return []
    s = s.replace('_', ' ')
    # try:
    #     s = unidecode(s.upper())
    # except Exception:
    s = s.upper()
    for person in persons:
        # p = unidecode(person['LastName'].upper())
        p = person['LastName'].upper()
        if len(p) > 2 and p in s:
            proposals.append(person)
    return proposals


def ontdubbel(persons):
    npersons = []
    for person in persons:
        if person not in npersons:
            npersons.append(person)
    return npersons


def filter_provided(proposals, persons):
    nproposals = []
    for proposal in proposals:
        found = False
        for person in persons:
            if proposal['FirstName'] == person['FirstName'] and proposal['LastName'] == person['LastName']:
                found = True
        if not found:
            nproposals.append(proposal)
    return nproposals


def get_proposals_from_piece(piece, persons, aliasses, fieldname):
    proposals = []
    proposals += has_person(piece[0], persons)
    proposals += has_alias(piece[0], aliasses, fieldname)
    return proposals


def get_proposals_from_cuesheet(cuesheet, persons, aliasses, fieldname):
    proposals = []
    proposals += has_person(cuesheet['Title'], persons)
    proposals += has_person(cuesheet['Filename'], persons)
    proposals += has_person(cuesheet['cue'].get('performer'), persons)
    proposals += has_alias(cuesheet['cue'].get('performer'), aliasses, fieldname)
    proposals += has_alias(cuesheet['Title'], aliasses, fieldname)
    proposals += has_alias(cuesheet['Filename'], aliasses, fieldname)
    for file in cuesheet['cue']['files']:
        if file:
            for track in file['tracks']:
                if track:
                    track_title = track.get('title')
                    if track_title:
                        proposals += has_alias(track_title, aliasses, fieldname)
                        proposals += has_person(track_title, persons)
    return proposals


def get_other_proposals(album, persons, aliasses, fieldname, album_persons):
    proposals = []
    proposals += has_person(album['Title'], persons)
    proposals += has_alias(album['Title'], aliasses, fieldname)
    return proposals


def filter_proposals(proposals, album_persons):
    proposals = ontdubbel(proposals)
    proposals = filter_provided(proposals, album_persons)
    return proposals


def get_proposals(cuesheets, pieces, album, album_componisten):
    componisten = get_componisten()
    aliasses = get_componist_aliasses()
    proposals = []
    for cuesheet in cuesheets:
        proposals += get_proposals_from_cuesheet(cuesheet,
                                                 componisten, aliasses,
                                                 'ComponistID')
    for piece in pieces:
        proposals += get_proposals_from_piece(piece, componisten, aliasses,
                                              'ComponistID')
    proposals += get_other_proposals(album, componisten, aliasses,
                                     'ComponistID', album_componisten)
    proposals = filter_proposals(proposals, album_componisten)
    return proposals


def get_artists(cuesheets, pieces, album, album_performers):
    performers = get_performers()
    aliasses = get_performer_aliasses()
    proposals = []
    for cuesheet in cuesheets:
        proposals += get_proposals_from_cuesheet(cuesheet, performers, aliasses,
                                                 'PerformerID')
    proposals += get_other_proposals(album, performers, aliasses, 'ComponistID',
                                     album_performers)
    proposals = filter_proposals(proposals, album_performers)
    return proposals


