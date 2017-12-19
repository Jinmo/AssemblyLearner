import json

import sqlalchemy
from flask import render_template, abort, request

from . import admin
from ...db import db_session
from ...db.models import Challenge
from ...forms import ChallengeForm
from ...library.pagination import Pagination
from ...middleware import *


@admin.route('/')
@admin_required
def index():
    return redirect('/admin/challenges')


@admin.route('/challenges')
@admin_required
def challenges():
    page = int(request.args.get('p', 1))
    div = 20

    problem_count = Challenge.query.count()
    problems = Challenge.list()

    pagination = Pagination(page, div, problem_count)

    return render_template('admin/problems.html', now='problem', pagination=pagination, problems=problems)


@admin.route('/challenge')
@admin.route('/challenge/<int:prob_id>')
@admin_required
def problem_form(prob_id=None, form=None):
    prob = None
    if (prob_id):
        prob = Challenge.get(prob_id)
        form = ChallengeForm(obj=prob)

    categories = json.dumps(
        db_session.query(sqlalchemy.distinct(Challenge.category)).all())

    return render_template('admin/problem_form.html', now='problem', problem=prob, categories=categories,
                           form=form if form else ChallengeForm())


@admin.route('/challenge', methods=['POST'])
@admin.route('/challenge/<int:prob_id>', methods=['POST'])
@admin_required
def add_problem(prob_id=None):
    form = ChallengeForm()
    if form.validate_on_submit():
        try:
            if prob_id:
                chal = Challenge.get(prob_id)
                if not chal:
                    return abort(404)
                chal.update(name=form.name.data, instruction=form.instruction.data, answer_regex=form.answer_regex.data,
                            suffix=form.suffix.data, example=form.example.data, category=form.category.data,
                            input=form.input.data, hint=form.hint.data)
            else:
                prob_id = Challenge.create(name=form.name.data, instruction=form.instruction.data,
                                           answer_regex=form.answer_regex.data,
                                           suffix=form.suffix.data, example=form.example.data,
                                           category=form.category.data, status='REG', input=form.input.data,
                                           hint=form.hint.data).save(True).id

            return redirect('/admin/challenge/' + str(prob_id))
        except Exception as e:
            print(e)
            return '''
                <script>
                    alert("Fail to add problems");
                    history.back(-1);
                </script>
            '''
    else:
        return problem_form(form=form)


@admin.route('/problem/<int:prob_id>/delete')
@admin_required
def delete_problem(prob_id):
    try:
        chal = Challenge.get(prob_id)
        if chal is None:
            return abort(404)
        chal.delete()
        return redirect('/admin/problems')
    except Exception as e:
        print(e)
