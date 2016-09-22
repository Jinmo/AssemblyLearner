import sqlite3
from os.path import isfile
import codecs


class DB:
    def __init__(self, dbPath='db.db'):
        db = sqlite3.connect(dbPath)
        db.row_factory = lambda cursor, row: dict((cursor.description[idx][0], value)
                                                  for idx, value in enumerate(row))
        self._db = db

    def query(self, query, args=None, isSingle=False):
        if args:
            cur = self._db.execute(query, args)
        else:
            cur = self._db.execute(query)

        rv = cur.fetchone() if isSingle is True else cur.fetchall()

        return rv

    def execute(self, query, args):
        cur = self._db.execute(query, args)
        row_id = cur.lastrowid
        cur.close()
        return row_id

    def rollback(self):
        self._db.rollback()

    def commit(self):
        self._db.commit()

    def executescript(self, path):
        if path is None or isfile(path) is False:
            raise Exception('File Not Found')

        f = codecs.open(path, 'r', 'utf8')
        query = f.read()
        f.close()

        self._db.executescript(query)
        self._db.commit()

    def __del__(self):
        self._db.close()
