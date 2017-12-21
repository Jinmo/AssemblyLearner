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
    name = request.form['name']
    password = request.form['password']
    role = request.form['role']

    try:
        assert (user_id is None or user_id and user_id == name)

        if user_id:
            user = User.get(user_id)
            user.update(
                True,
                password=password,
                role=role
            )
        else:
            user = User.create(
                name=name,
                password=password,
                role=role
            )
            user.save(True)

        return redirect('/admin/user/%d' % user.id)
    except Exception as e:
        return '''
            <script>
                alert("Fail to add user");
                history.back(-1);
            </script>
        '''
