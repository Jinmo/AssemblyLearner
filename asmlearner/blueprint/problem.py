from flask import Blueprint, render_template, abort, g, session, redirect
from jinja2 import TemplateNotFound
from asmlearner.middleware import *
from hashlib import sha1

problem = Blueprint('prob', __name__)


@problem.route('/problems')
@login_required
def problem_list():
    return render_template('problems.html', title='Problems') 