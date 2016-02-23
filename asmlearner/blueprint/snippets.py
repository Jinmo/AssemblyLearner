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
        snippet = g.db.query('SELECT s.id, s.filename, s.code FROM snippets AS s WHERE id=? AND owner=?', (snippet_id, session['user']['id']), True)
    else:
        snippet = None

    return render_template('snippet_form.html', title='Snippet edit', snippet=snippet)

def save_snippet(owner, filename, code):
    return

@snippets.route('/snippet/', methods=['POST'])
@snippets.route('/snippet/<int:snippet_id>', methods=['POST'])
@login_required
def snippet_upload(snippet_id=None):
    filename = request.form['filename']
    code = request.form['code']

    owner = session['user']['id']
    if snippet_id is not None:
        try:
            g.db.query('UPDATE snippets SET filename=?, code=? WHERE id=? AND owner=?', (filename, code, snippet_id, owner))
            g.db.commit()
        except Exception as e:
            print e
            g.db.rollback()
            return ''
    else:
        try:
            g.db.query('INSERT INTO snippets(filename,code,owner) VALUES(?,?,?)', (filename, code, owner))
            g.db.commit()
        except Exception as e:
            print e
            g.db.rollback()
            return ''

    save_snippet(owner, filename, code)
    return redirect('/snippets')
