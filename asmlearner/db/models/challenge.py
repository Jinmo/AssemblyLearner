import datetime
import asmlearner.library.markdown

from flask import Markup
from asmlearner.db.base import Base, IdMixin
from sqlalchemy import Column, String, Text, DateTime


class Challenge(Base, IdMixin):
    name = Column(String(200), unique=True)
    instruction = Column(Text, nullable=False)
    answer_regex = Column(Text, nullable=False)
    suffix = Column(Text, nullable=False)
    example = Column(Text)
    status = Column(String(10))
    category = Column(String(50))
    input = Column(Text)
    hint = Column(Text)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def list(cls):
        return cls.query.order_by(cls.id.asc())

    def instruction_formatted(self):
        return Markup(asmlearner.library.markdown.markdown(self.instruction))
