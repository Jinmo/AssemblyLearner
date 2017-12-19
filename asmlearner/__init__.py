import time

from flask import Flask, g, request, url_for
from flask_login import LoginManager

from .blueprint import user, problem, admin, snippets, history, index
from .config import config
from .db import db_session, Base, engine
from .db.models import User

from urllib import quote

app = Flask(__name__)
app.config.from_object(config)
app.debug = True

login_manager = LoginManager(app)
login_manager.login_view = 'user.login'


@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))


app.register_blueprint(user)
app.register_blueprint(problem)
app.register_blueprint(snippets)
app.register_blueprint(admin)
app.register_blueprint(history)
app.register_blueprint(index)


def url_for_other_page(page):
    args = request.view_args.copy()
    args['p'] = page
    return url_for(request.endpoint, **args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['quote'] = quote

with app.app_context():
    g.updated_time = time.time()


@app.teardown_request
def teardown(ctx):
    try:
        db_session.commit()
    finally:
        db_session.remove()


def create_db():
    Base.metadata.bind = engine
    return Base.metadata.create_all()
