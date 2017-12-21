from flask import Blueprint, redirect, session
from flask_login import login_required

index = Blueprint('index', __name__)


@index.route('/')
@login_required
def index_():
    return redirect('/challenges')
