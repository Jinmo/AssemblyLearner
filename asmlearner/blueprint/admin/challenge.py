import json

import sqlalchemy
from flask import render_template, abort, request, jsonify

from . import admin
from ...db import db_session
from ...db.models import Challenge
from ...forms import ChallengeForm
from ...middleware import *


@admin.route('/')
@admin_required
def index():
    return redirect('/admin/challenges')


@admin.route('/challenges')
@admin_required
def challenges():
    challenges = Challenge.list()
    return render_template('admin/challenges.html', now='challenge', challenges=challenges)


@admin.route('/challenge')
@admin.route('/challenge/<int:prob_id>')
@admin_required
def challenge_form(prob_id=None, form=None):
    prob = None
    if (prob_id):
        prob = Challenge.get(prob_id)
        form = ChallengeForm(obj=prob)

    categories = json.dumps(
        db_session.query(sqlalchemy.distinct(Challenge.category)).all())

    return render_template('admin/challenge_form.html', now='challenge', challenge=prob, categories=categories,
                           form=form if form else ChallengeForm())


@admin.route('/challenge', methods=['POST'])
@admin.route('/challenge/<int:prob_id>', methods=['POST'])
@admin_required
def add_challenge(prob_id=None):
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
                    alert("Fail to add challenges");
                    history.back(-1);
                </script>
            '''
    else:
        return challenge_form(form=form)


@admin.route('/challenge/<int:prob_id>/delete')
@admin_required
def delete_challenge(prob_id):
    try:
        chal = Challenge.get(prob_id)
        if chal is None:
            return abort(404)
        chal.delete()
        return redirect('/admin/challenges')
    except Exception as e:
        print(e)


@admin.route('/challenges/save_order', methods=['POST'])
@admin_required
def save_challenge_order():
    data = request.get_json(force=True)
    for cid, order_key in data:
        cid = int(cid)
        item = Challenge.get(cid)
        if item is None:
            continue
        item.update(orderKey=order_key)
    return jsonify(success=True)
