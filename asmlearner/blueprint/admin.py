from flask import Blueprint, render_template, abort, g, session, redirect
from jinja2 import TemplateNotFound
from asmlearner.middleware import *
import json

admin = Blueprint('admin', __name__)

@admin.route('/')
def index():
    return redirect('/admin/problems')

@admin.route('/problems')
@is_admin
def problems():
    return render_template('admin/problems.html', now='problem')

@admin.route('/problem')
@is_admin
def problem_form():
    return render_template('admin/problem_form.html', now='problem', action='/admin/problem')

@admin.route('/problem', methods=['POST'])
@is_admin
def add_problem():
    name = request.form['prob_name']
    instr = request.form['prob_instruction']
    suffix = request.form['prob_suffix']
    example = request.form['prob_example']        
    answ = request.form['prob_answer']
    tag = request.form['tags']

    return json.dumps(request.form)

@admin.route('/users')
@is_admin
def users():
    return render_template('admin/users.html', now='user')