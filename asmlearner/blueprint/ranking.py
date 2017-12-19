# coding:utf8

from flask import Blueprint, render_template, g
from asmlearner.middleware import *

ranking = Blueprint('ranking', __name__)


@ranking.route('/ranking')
def ranking():
    return render_template('ranking.html')
