from asmlearner import config
from asmlearner.library.database.sqlite import DB
from os.path import join
import getpass
from hashlib import sha1


db = DB(config.DATABASE)
db.executescript(join(config.PROJECT_DIR, 'init.sql'))
id_ = raw_input('ID: ')
password_ = getpass.getpass('PW: ')
pw_hash = sha1(password_ * 10).hexdigest()

db.commit('INSERT INTO user (id, password, role) VALUES(?, ?, \'admin\')', (id_, pw_hash))

