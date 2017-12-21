from functools import wraps
from flask import session, redirect
from flask_login import login_required, current_user

login_required = login_required


def admin_required(f):
    @wraps(f)
    def func(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'admin':
            return f(*args, **kwargs)

        return redirect('/challenges')

    return func
