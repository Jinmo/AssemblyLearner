from flask import Blueprint, render_template, g
from asmlearner.middleware import *
from asmlearner.library.pagination import Pagination

import os
import codecs, binascii

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
    owner_encoded = binascii.hexlify( bytes(owner, 'utf-8') ).decode('utf-8')
    snippet_dir = 'data/snippets/' + owner_encoded
    snippet_path = os.path.join(snippet_dir, filename)

    if os.path.isdir(snippet_dir) == False:
        os.makedirs(snippet_dir)
    with open(snippet_path, 'wb') as f:
        f.write(bytes(code, 'utf-8'))
    return

@snippets.route('/snippet/', methods=['POST'])
@snippets.route('/snippet/<int:snippet_id>', methods=['POST'])
@login_required
def snippet_upload(snippet_id=None):
    filename = request.form['filename']
    code = request.form['code']

    owner = session['user']['id']

    filename = os.path.basename(filename)
    if snippet_id is not None:
        try:
            g.db.query('UPDATE snippets SET filename=?, code=? WHERE id=? AND owner=?', (filename, code, snippet_id, owner))
            g.db.commit()
            save_snippet(owner, filename, code)
        except Exception as e:
            print(e)
            g.db.rollback()
            return ''
    else:
        try:
            g.db.query('REPLACE INTO snippets(filename,code,owner) VALUES(?,?,?)', (filename, code, owner))
            g.db.commit()
            save_snippet(owner, filename, code)
        except Exception as e:
            print(e)
            g.db.rollback()
            return ''

    return redirect('/snippets')
