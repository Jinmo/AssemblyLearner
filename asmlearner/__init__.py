from os.path import join, dirname, realpath

from flask import Flask, g
from blueprint.user import user
from lib.database.sqlite import DB

CURPATH = dirname(realpath(__file__))
DATABASE = join(CURPATH, 'db.db')

app = Flask(__name__, static_url_path='')
app.register_blueprint(user)

@app.before_request
def before_req():
    g.db = DB(DATABASE);
