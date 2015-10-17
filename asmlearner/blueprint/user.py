from flask import Blueprint, render_template, abort, g, session, redirect
from jinja2 import TemplateNotFound
from asmlearner.middleware import *

user = Blueprint('user', __name__, template_folder='view')

@user.route('/login')
def login():
    render_template('login.html')

@user.route('/logout')
@login_required
def logout():
    del session['user']
    redirect('/')
