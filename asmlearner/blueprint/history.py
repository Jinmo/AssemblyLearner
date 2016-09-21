from flask import Blueprint, render_template, g, redirect, jsonify
from asmlearner.middleware import *
from asmlearner.library.pagination import Pagination

history = Blueprint('history', __name__)

@history.route('/histories')
@login_required
def history_list():
    page = int(request.args.get('p') if 'p' in request.args else '1')
    div = 20
    user_id = session['user']['id']
    histories = g.db.query('SELECT s.id, s.status, s.problem, (SELECT p.name FROM problem as p WHERE p.id = s.problem) AS probname FROM solved AS s WHERE owner=? ORDER BY time DESC LIMIT ?, ?', (user_id, (page-1)*div, div))
    history_count = g.db.query('SELECT COUNT(1) AS cnt FROM solved WHERE owner=?', (user_id, ), isSingle=True)['cnt']
    pagination = Pagination(page, div, history_count)

    return render_template('history.html', histories=histories, pagination=pagination)

def get_history(history_id):
    history = g.db.query('SELECT * FROM solved AS s WHERE s.id=?', (history_id, ),
            isSingle=True)
    return history

@history.route('/api/history/<int:history_id>')
@login_required
def history_api(history_id):
    user_id = session['user']['id']
    history = get_history(history_id)
    if history is not None and history['owner'] != user_id:
        history = None

    return jsonify(history if history is not None else {})

@history.route('/history/<int:history_id>')
@login_required
def history_(history_id):
    user_id = session['user']['id']
    history = get_history(history_id)
    snippet = {}

    if history is not None:
        snippet['code'] = history['answer']
        snippet['id'] = history['id']

    if history is not None and history['owner'] != user_id:
        history = None

    history = history if history is not None else {}

    return render_template('history_form.html', snippet=snippet)
