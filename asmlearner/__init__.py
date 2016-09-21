from os.path import join, dirname, realpath
from time import time

from flask import Flask, g, redirect, session, url_for, request
from asmlearner.blueprint import user, problem, admin, snippets, history
from asmlearner.library.database.sqlite import DB
import asmlearner.config


app = Flask(__name__, static_url_path='')

app.register_blueprint(user)
app.register_blueprint(problem)
app.register_blueprint(snippets)
app.register_blueprint(admin)
app.register_blueprint(history)

with app.app_context():
    g.updated_time = time()

@app.before_request
def before_req():
    g.db = DB(config.DATABASE)


@app.route('/')
def index():
    if 'user' in session:
        return redirect('/problems')
    else:
        return redirect('/login')

def is_admin():
    return ('user' in session) and (session['user']['role'] == 'admin')

def url_for_other_page(page):
    args = request.view_args.copy()
    args['p'] = page
    return url_for(request.endpoint, **args)

app.jinja_env.globals.update(url_for_other_page=url_for_other_page)
app.jinja_env.globals.update(is_admin=is_admin)
