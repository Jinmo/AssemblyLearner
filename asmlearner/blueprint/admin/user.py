from flask import Blueprint, render_template, abort, g, session, redirect
from jinja2 import TemplateNotFound
from asmlearner.middleware import *
from asmlearner.library.pagination import Pagination
import json
from . import admin

@admin.route('/users')
@is_admin
def users():
    return render_template('admin/users.html', now='user')