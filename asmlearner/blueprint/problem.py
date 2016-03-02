#coding:utf8

from flask import Blueprint, render_template, abort, g, session, redirect, jsonify
from jinja2 import TemplateNotFound
from asmlearner.middleware import *
from hashlib import sha1
from asmlearner.library.pagination import Pagination
from asmlearner.library.compiler.asm import compileProblem
from redis import Redis
from rq import Queue

q = Queue(connection=Redis())
problem = Blueprint('prob', __name__)

@problem.route('/problems')
@login_required
def problem_list():
    page = int(request.args.get('p')) if 'p' in request.args else 1
    div = 20
    user_id = session['user']['id']

    problem_count = g.db.query('SELECT count(*) as count FROM problem', isSingle=True)['count']
    problems = g.db.query('SELECT p.id,p.name,p.category FROM problem as p limit ?,?', ((page-1)*div, div))
    solved = g.db.query('SELECT s.problem FROM solved as s WHERE owner=? AND status="CORRECT"', user_id)

    problems_map = {}

    for problem in problems:
        problems_map[problem['id']] = problem

    for item in solved:
        problems_map[item['problem']]['solved'] = True

    pagination = Pagination(page, div, problem_count)
    return render_template('problems.html', title='Problems', pagination=pagination, problems=problems)

@problem.route('/problem/<int:prob_id>')
@login_required
def problem_(prob_id):
    problem = g.db.query('SELECT p.id,p.name,p.category,p.answer_regex,p.instruction,p.suffix,p.example,p.category,p.status FROM problem AS p WHERE id=?', (prob_id,), True)

    return render_template('problem.html', title=':: ' + problem['name'], problem=problem)

@problem.route('/problem/<int:prob_id>/submit', methods=['POST'])
@login_required
def problem_run(prob_id):
    code = request.form['code']
    user_id = session['user']['id']

    try:
        prob = g.db.query('SELECT * FROM problem where id = ?', (prob_id,), isSingle=True)
        solved_id = g.db.execute('INSERT INTO solved ( ' \
                    'problem, owner, status, answer, errmsg) VALUES ' \
                    '(?, ?, ?, ?, ?)', (prob_id, user_id, 'COMPILE', code, ''))
        g.db.commit()

        solved = g.db.query('SELECT * FROM solved where id = ?', (solved_id,), isSingle=True)
        q.enqueue(compileProblem, prob, solved)
        return jsonify(status='success', sid=solved_id)
    except Exception as e:
        print(e)
        g.db.rollback()
        return jsonify(status='fail')

@problem.route('/answer/<int:as_id>/status', methods=['POST'])
@login_required
def answer_status(as_id):
    ans = g.db.query('SELECT * FROM solved where id = ?', (as_id,), isSingle=True)

    if (ans == None):
        return abort(404)

    return jsonify(status=ans['status'])
