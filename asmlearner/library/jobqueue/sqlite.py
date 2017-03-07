# queue implemented in sqlite

from asmlearner.library.database.sqlite import DB
from asmlearner import config
import time
import json
import sys
import traceback

def importModule(name):
    mod = __import__(name)
    comps = name.split('.')
    for comp in comps[1:]:
        mod = getattr(mod, comp)

    return mod

class Queue:

    def get_db(self):
        db = DB(config.DATABASE)
        return db

    def enqueue(self, func, args):
        db = self.get_db()
        db.execute('INSERT INTO queue(func, args) VALUES(?, ?)', (func, json.dumps(args)))
        db.commit()

    def dequeue(self):
        db = self.get_db()
        job = db.query('SELECT * FROM queue LIMIT 1', isSingle=True)
        if job is None:
            time.sleep(0.5)
            return

        id_ = job['id']
        func = job['func']
        args = job['args']
        args = json.loads(args)

        try:
            module = func.split('.')[:-1]
            module = '.'.join(module)

            func = func.split('.')[-1]
            module = importModule(module)
            func = getattr(module, func)

            func(*args)

            db.execute('DELETE FROM queue WHERE id=?', (id_, ))
            db.commit()
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            pass

def cli():
    q = Queue()
    while True:
        q.dequeue()
