from .challenge import Challenge
from .user import User
from ..base import Base, IdMixin, ForeignMixin
from ...tasks import compiler

from sqlalchemy import Column, Text, String, Binary


class History(Base, IdMixin, ForeignMixin('chal', Challenge), ForeignMixin('owner', User)):
    code = Column(Binary)
    errmsg = Column(Binary)
    status = Column(String(100))

    def enqueue(self):
        compiler.delay(self.id)
