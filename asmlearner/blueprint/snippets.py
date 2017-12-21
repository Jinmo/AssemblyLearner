import os

from flask import Blueprint, render_template, abort, request

from asmlearner.db.models import Snippet
from asmlearner.library.pagination import Pagination
from asmlearner.middleware import *

snippets = Blueprint('snippets', __name__)


@snippets.route('/snippets')
@login_required
def snippet_list():
    page = int(request.args.get('p', 1))
    div = 20

    q = Snippet.query.filter(Snippet.owner_id == current_user.id)
    snippets = q.offset((page - 1) * div).limit(div)

    pagination = Pagination(page, div, q.count())
    return render_template('snippets.html', title='Snippets', pagination=pagination, snippets=snippets)


@snippets.route('/snippet/')
@snippets.route('/snippet/<int:snippet_id>')
@login_required
def snippet_form(snippet_id=None, form=None):
    if snippet_id is not None:
        snippet = Snippet.find(snippet_id, current_user)
        if not snippet:
            return abort(404)
    else:
        snippet = None

    return render_template('snippet_form.html', title='Snippet edit', snippet=snippet)


@snippets.route('/snippet/', methods=['POST'])
@snippets.route('/snippet/<int:snippet_id>', methods=['POST'])
@login_required
def snippet_upload(snippet_id=None):
    filename = request.form['filename']
    code = request.form['code']

    filename = os.path.basename(filename)
    if snippet_id is not None:
        try:
            snippet = Snippet.find(snippet_id, current_user)
            snippet.update(True, name=filename)
            snippet.data = code
        except Exception as e:
            raise
    else:
        try:
            snippet = Snippet.create(name=filename.split('/')[-1].split('\\')[-1], owner_id=current_user.id)
            snippet.save(True)
            snippet.data = code
        except Exception as e:
            raise

    return redirect('/snippets')
