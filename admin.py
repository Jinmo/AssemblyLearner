#!/usr/bin/python3

from asmlearner.db import db_session
from asmlearner.db.models import User
import getpass

id_ = raw_input('ID: ')
password_ = getpass.getpass('PW: ')

db_session.add(User.create(name=id_, password=password_, role='admin'))
db_session.commit()
