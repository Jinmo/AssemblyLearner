# coding:utf8

from flask import Blueprint, render_template, abort, session, jsonify, request
from flask_login import current_user
from asmlearner.middleware import login_required
from asmlearner.library.pagination import Pagination
from asmlearner.db.models import Challenge, History

challenge = Blueprint('challenge', __name__)


@challenge.route('/challenges')
@login_required
def list_challenge():
    page = int(request.args.get('p', 1))
    div = 20

    challenges = Challenge.list()
    pagination = Pagination(page, div, challenges.count())
    return render_template('challenges.html', title='Challenges', pagination=pagination, challenges=challenges)


@challenge.route('/challenge/<int:prob_id>')
@login_required
def view_challenge(prob_id):
    chal = Challenge.get(prob_id)

    from sqlalchemy.dialects import postgresql
    print History.query.filter(History.chal_id == prob_id, History.owner_id == int(current_user.id)).statement.compile(
        dialect=postgresql.dialect())
    history = History.query.filter(History.chal_id == prob_id, History.owner_id == int(current_user.id)).order_by(
        History.id.desc()).first()
    if history:
        saved_code = history.code
    else:
        saved_code = ''

    return render_template('challenge.html', title=':: ' + chal.name, chal=chal, saved_code=saved_code)


@challenge.route('/challenge/<int:prob_id>/submit', methods=['POST'])
@login_required
def run_challenge(prob_id):
    code = request.form['code']

    try:
        log = History.create(chal_id=prob_id, owner_id=int(current_user.id), status='COMPILE',
                             code=code.encode('utf-8'), errmsg='')
        log.save(True)
        log.enqueue()

        return jsonify(status='success', sid=log.id)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
        return jsonify(status='fail')


@challenge.route('/answer/<int:as_id>/status')
@login_required
def answer_status(as_id):
    ans = History.get(as_id, current_user).first()

    if not ans:
        return abort(404)

    return jsonify(status=ans.status, errmsg=ans.errmsg.encode('base64'))

