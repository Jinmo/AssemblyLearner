from flask import Blueprint

admin = Blueprint('admin', __name__, url_prefix='/admin')

from .problem import *
from .user import *
