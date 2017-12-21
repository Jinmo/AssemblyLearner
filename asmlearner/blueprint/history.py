from flask import Blueprint, render_template, request, jsonify, abort
from asmlearner.middleware import *
from asmlearner.library.pagination import Pagination
from asmlearner.db.models import History

history = Blueprint('history', __name__)


@history.route('/histories')
@login_required
def history_list():
    page = int(request.args.get('p', 1))
    div = 20
    histories = History.query.filter(History.owner_id == current_user.id).order_by(History.id.desc()).offset((page - 1) * div).limit(div)
    pagination = Pagination(page, div, histories.count())

    return render_template('history.html', histories=histories, pagination=pagination)


def get_history(history_id):
    h = History.get(history_id)
    if current_user.id != h.owner_id:
        return None
    return h


@history.route('/api/history/<int:history_id>')
@login_required
def history_api(history_id):
    hist = get_history(history_id)
    if hist is None and hist.owner_id != current_user.id:
        return abort(404)

    return jsonify(hist)


@history.route('/history/<int:history_id>')
@login_required
def history_(history_id):
    history = get_history(history_id)

    if history and history.owner_id != current_user.id:
        return abort(404)

    return render_template('history_form.html', history=history, snippet={
        'data': history.code,
        'name': '#%d-%d' % (history.chal_id, history.id),
        'output': history.errmsg
    }, additional_properties='readonly', code_only=True)
