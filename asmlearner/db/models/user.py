from asmlearner.db import Base, IdMixin
from sqlalchemy_utils import PasswordType
from sqlalchemy import Column, String, Boolean

ID_LEN = 256
ROLE_LEN = 256


class User(Base, IdMixin):
    name = Column(String(ID_LEN), unique=True)
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512'
        ]
    ))
    role = Column(String(ROLE_LEN), default='user')
    is_active = Column(Boolean, default=True)

    @property
    def is_authenticated(cls):
        return True

    @property
    def is_anonymous(cls):
        return False

    def get_id(self):
        return str(self.id)

    @classmethod
    def login(cls, name, password):
        user = cls.query.filter(cls.name == name).first()
        if not user:
            return None
        if user.password == password:
            return user
        return None

    @classmethod
    def by_name(cls, name):
        return cls.query.filter(cls.name == name).first()

    @classmethod
    def exists(cls, name):
        return cls.query.filter(cls.name == name).count() != 0

    def solved(cls, chal):
        from .history import History
        return History.query.filter(History.chal_id == chal.id, History.owner_id == cls.id,
                                    History.status == 'CORRECT').count() != 0

    pass
