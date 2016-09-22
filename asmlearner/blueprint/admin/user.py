from flask import Blueprint, render_template, abort, g, session, redirect
from jinja2 import TemplateNotFound
from asmlearner.middleware import *
from asmlearner.library.pagination import Pagination
from hashlib import sha1
import json
from . import admin


@admin.route('/')
@is_admin
def user_index():
    return redirect('/admin/users')


@admin.route('/users')
@is_admin
def users():
    page = int(request.args.get('p')) if 'p' in request.args else 1
    div = 20

    user_count = g.db.query('SELECT count(*) as count FROM user', isSingle=True)['count']
    users = g.db.query('SELECT u.id, u.password, u.role FROM user as u group by u.id limit ?,?',
                       ((page - 1) * div, div))

    pagination = Pagination(page, div, user_count)

    return render_template('admin/users.html', now='user', pagination=pagination, users=users)


@admin.route('/user')
@admin.route('/user/<user_id>')
@is_admin
def user_form(user_id=None):
    user = None
    if (user_id):
        user = g.db.query('SELECT * FROM user where id=?', (user_id,), True)

    return render_template('admin/user_form.html', now='user', user=user)


@admin.route('/user', methods=['POST'])
@admin.route('/user/<user_id>', methods=['POST'])
@is_admin
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
