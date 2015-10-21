from os.path import join, dirname, realpath

from flask import Flask, g, redirect, session, url_for, request
from blueprint import user, problem, admin
from library.database.sqlite import DB
import config


app = Flask(__name__, static_url_path='')

app.register_blueprint(user)
app.register_blueprint(problem)
app.register_blueprint(admin)


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
    args['page'] = page
    return url_for(request.endpoint, **args)

app.jinja_env.globals.update(url_for_other_page=url_for_other_page)
app.jinja_env.globals.update(is_admin=is_admin)