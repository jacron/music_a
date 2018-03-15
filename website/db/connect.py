from django.conf import settings
import sqlite3

from music.settings import SQLITE3_FILE


def connect():
    conn = sqlite3.connect(SQLITE3_FILE)
    c = conn.cursor()
    return conn, c


