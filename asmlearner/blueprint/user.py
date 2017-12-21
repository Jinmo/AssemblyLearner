from flask import Blueprint, render_template, session, redirect, request, flash
from flask_login import login_user, logout_user
from asmlearner.middleware import login_required
from asmlearner.forms.user import LoginForm, RegisterForm

user = Blueprint('user', __name__)


@user.route('/login')
def login(form=None):
    return render_template('login.html', title='AL User Login', action='/login', submit='Login', next_link='/join',
                           next='Create User', form=form if form else LoginForm())


@user.route('/login', methods=['POST'])
def login_check():
    form = LoginForm()

    if not form.validate_on_submit():
        flash('ID or PW is incorrect')
        return login()
    else:
        login_user(form.user)
        return redirect('/challenges')


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@user.route('/join')
def join(form=None):
    return render_template('login.html', title="AL User Create", action="/join", submit='Join', next_link='/login',
                           next='Login As User', form=form if form else RegisterForm())


@user.route('/join', methods=['POST'])
def join_check():
    form = RegisterForm()

    if form.validate_on_submit():
        flash('Successfully created a user!')
        return redirect('/login')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))
        flash('User with the specified name already exists!')
        return join()
