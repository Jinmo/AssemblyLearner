from .. import Base, IdMixin, ForeignMixin
from ...config import config
from sqlalchemy import Integer, String, Column
from .user import User
from ...library.snippets import save_snippet

import os


class Snippet(Base, IdMixin, ForeignMixin('owner', User)):
    name = Column(String(256), unique=True)

    @property
    def data(self):
        saved_code_path = os.path.join(config.SNIPPET_PATH, str(self.owner_id), self.name)

        if os.path.isfile(saved_code_path):
            with open(saved_code_path, 'rb') as saved_code:
                saved_code = saved_code.read()
        else:
            saved_code = ''
        return saved_code

    @data.setter
    def data(self, code):
        save_snippet(self.owner, self.name, code)
