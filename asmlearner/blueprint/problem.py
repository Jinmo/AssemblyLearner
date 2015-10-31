from flask import Blueprint, render_template, abort, g, session, redirect
from jinja2 import TemplateNotFound
from asmlearner.middleware import *
from hashlib import sha1
from asmlearner.library.pagination import Pagination

problem = Blueprint('prob', __name__)


@problem.route('/problems')
@login_required
def problem_list():
    page = int(request.args.get('p')) if 'p' in request.args else 1
    div = 20

    problem_count = g.db.query('SELECT count(*) as count FROM problem', isSingle=True)['count']
    problems = g.db.query('SELECT p.id,p.name,p.category FROM problem as p limit ?,?', ((page-1)*div, div))

    pagination = Pagination(page, div, problem_count)
    return render_template('problems.html', title='Problems', pagination=pagination, problems=problems)
