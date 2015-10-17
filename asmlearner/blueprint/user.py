from flask import Blueprint, render_template, abort, g, session, redirect
from jinja2 import TemplateNotFound
from asmlearner.middleware import *

user = Blueprint('user', __name__, template_folder='view')

@user.route('/login')
def login():
    return render_template('login.html', title='AL User Login', action='/login', submit='Login')

@user.route('/login', methods=['POST'])
def login_check():
    return ''

@user.route('/logout')
@login_required
def logout():
    del session['user']
    redirect('/')

@user.route('/join')
def join():
    return render_template('login.html', title="AL User Create", action="/join", submit='Join')

@user.route('/join', methods=['POST'])
def join_check():
    return ''
