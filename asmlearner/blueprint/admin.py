from flask import Blueprint, render_template, abort, g, session, redirect
from jinja2 import TemplateNotFound
from asmlearner.middleware import *

admin = Blueprint('admin', __name__)

@admin.route('/')
def index():
    return redirect('/admin/problems')

@admin.route('/problems')
@is_admin
def problems():
    return render_template('admin/problems.html')