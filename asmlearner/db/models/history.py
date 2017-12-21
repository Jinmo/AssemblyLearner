from .challenge import Challenge
from .user import User
from ..base import Base, IdMixin, ForeignMixin
from ...tasks import compiler

from sqlalchemy import Column, String, Binary, Boolean, or_


class History(Base, IdMixin, ForeignMixin('chal', Challenge), ForeignMixin('owner', User)):
    code = Column(Binary)
    errmsg = Column(Binary)
    status = Column(String(100))
    is_public = Column(Boolean, default=False)

    def enqueue(self):
        compiler.delay(self.id)

    @classmethod
    def get(cls, id, user=None, worker=False):
        if user is None and not worker:
            raise Exception('user field on history is mandatory')
        return cls.query.filter(cls.id == id, or_(cls.is_public, cls.owner_id == user.id))
