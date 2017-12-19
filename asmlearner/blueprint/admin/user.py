from hashlib import sha1

from flask import render_template, g, request

from asmlearner.library.pagination import Pagination
from asmlearner.middleware import *
from . import admin
from ...db.models import User


@admin.route('/')
@admin_required
def user_index():
    return redirect('/admin/users')


@admin.route('/users')
@admin_required
def users():
    page = int(request.args.get('p', 1))
    div = 20

    user_count = User.query.count()
    users = User.query.offset((page - 1) * div).limit(div)

    pagination = Pagination(page, div, user_count)

    return render_template('admin/users.html', now='user', pagination=pagination, users=users)


@admin.route('/user')
@admin.route('/user/<user_id>')
@admin_required
def user_form(user_id=None):
    user = None
    if (user_id):
        user = User.get(user_id)

    return render_template('admin/user_form.html', now='user', user=user)


@admin.route('/user', methods=['POST'])
@admin.route('/user/<user_id>', methods=['POST'])
@admin_required
def add_user(user_id=None):
    id_ = request.form['id']
    password_ = request.form['password']
    role = request.form['role']

    pw_hashobj = sha1(password_ * 10)
    pw_hash = pw_hashobj.hexdigest()
    del password_, pw_hashobj

    try:
        assert (user_id is None or user_id and user_id == id_)

        if user_id:
            g.db.execute('UPDATE user SET password=?, role=? WHERE id=?', (pw_hash, role, user_id))
        else:
            user_id = g.db.execute('INSERT INTO user (' \
                                   'id, user, role) VALUES ' \
                                   '(?, ?, ?)', (id_, pw_hash, ''))

            g.db.commit()
        return redirect('/admin/users')
    except Exception as e:
        print(e)
        g.db.rollback()
        return '''
            <script>
                alert("Fail to add user");
                history.back(-1);
            </script>
        '''
