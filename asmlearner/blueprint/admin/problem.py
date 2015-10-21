from flask import Blueprint, render_template, abort, g, session, redirect
from jinja2 import TemplateNotFound
from asmlearner.middleware import *
from asmlearner.library.pagination import Pagination
import json
from . import admin

@admin.route('/')
def index():
    return redirect('/admin/problems')

@admin.route('/problems')
@is_admin
def problems():
    page = int(request.args.get('p')) if 'p' in request.args else 1
    div = 20    

    problem_count = g.db.query('SELECT count(*) as count FROM problem', isSingle=True)['count']
    problems = g.db.query('SELECT p.id,p.name,p.status,Group_Concat(t.name) tag FROM problem as p inner join tag as t on p.name=t.problem_name group by p.name limit ?,?', ((page-1)*div, div))
    print problems
    pagination = Pagination(page, div, problem_count)

    return render_template('admin/problems.html', now='problem', pagination=pagination, problems=problems)

@admin.route('/problem')
@admin.route('/problem/<int:prob_id>')
@is_admin
def problem_form(prob_id=None):
    prob=None
    if (prob_id):
        prob = g.db.query('SELECT * FROM problem where id=?', (prob_id,), True)
        tag = g.db.query('SELECT * FROM tag where problem_name=?', (prob['name'],))
        prob['tag'] = ','.join(list(map(lambda x: x['name'], tag)))
        
    return render_template('admin/problem_form.html', now='problem', problem=prob)

@admin.route('/problem', methods=['POST'])
@admin.route('/problem/<int:prob_id>', methods=['POST'])
@is_admin
def add_problem():
    name = request.form['prob_name']
    instr = request.form['prob_instruction']
    suffix = request.form['prob_suffix']
    example = request.form['prob_example']        
    answ = request.form['prob_answer']
    tag = request.form['tags'].split(',')

    try:
        g.db.execute('INSERT INTO problem (' \
            'name, instruction, answer_regex, suffix, ' \
            'example, status) VALUES ' \
        '(?, ?, ?, ?, ?, ?)', (name, instr, answ, suffix, example, 'REG'))
        
        g.db.execute('DELETE FROM tag where problem_name=?', (name,))
        
        for i in tag:
            g.db.execute('INSERT INTO tag (name, problem_name) VALUES (?, ?)', (i, name))

        g.db.commit()
        return redirect('/admin/problems')
    except Exception as e:
        print e
        g.db.rollback()
        return '''
            <script>
                alert("Fail to add problems");
                history.back(-1);
            </script>       
        '''