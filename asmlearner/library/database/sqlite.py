import sqlite3
from os.path import isfile

class DB:
    def __init__(self, dbPath='db.db'):
        db = sqlite3.connect(dbPath)
        db.row_factory = lambda cursor, row: dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
        self._db = db

    def execute(self, query, args, one=False):
        cur = self._db.execute(query, args)
        if one:
            rv = cur.fetchone()
        else:
            rv = cur.fetchall()

        return rv

    def commit(self, query, args):
        cur = self._db.execute(query, args)
        cur.close()
        self._db.commit()

    def executescript(self, path):
        if path == None or isfile(path) == False:
            raise Exception('File Not Found')

        f = open(path, 'rb')
        query = f.read()
        f.close()

        self._db.executescript(query)
        self._db.commit()       
