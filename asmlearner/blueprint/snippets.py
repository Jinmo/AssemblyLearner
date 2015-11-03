from flask import Blueprint, render_template, g
from asmlearner.middleware import *
from asmlearner.library.pagination import Pagination

snippets = Blueprint('snippets', __name__)


@snippets.route('/snippets')
@login_required
def snippet_list():
    page = int(request.args.get('p')) if 'p' in request.args else 1
    div = 20

    snippet_count = g.db.query('SELECT count(*) as count FROM snippets WHERE owner=?', (session['user']['id'],), isSingle=True)['count']
    snippets = g.db.query('SELECT * FROM snippets limit ?,?', ((page-1)*div, div))

    pagination = Pagination(page, div, snippet_count)
    return render_template('snippets.html', title='Snippets', pagination=pagination, snippets=snippets)

@snippets.route('/snippet/')
@snippets.route('/snippet/<int:snippet_id>')
@login_required
def snippet_form(snippet_id=None):
    if snippet_id is not None:
        snippet = g.db.query('SELECT s.id, s.filename FROM snippets AS s WHERE snippet_id=? AND owner=?', (snippet_id, session['user']['id']), True)
    else:
        snippet = None

    return render_template('snippet.html', snippet=snippet)
