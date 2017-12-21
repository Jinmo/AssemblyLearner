from flask import Blueprint

admin = Blueprint('admin', __name__, url_prefix='/admin')

from .challenge import *
from .user import *
