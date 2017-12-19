from sqlalchemy import Column, Integer, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from ..config import config


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def save(self, commit=False):
        db_session.add(self)
        if commit:
            db_session.commit()
        return self

    def delete(self, commit=False):
        db_session.delete(self)
        return commit and db_session.commit()

    def update(self, commit=False, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db_session.add(self)
        return commit and db_session.commit()

    pass


class BaseModel(CRUDMixin, object):
    pass


engine = create_engine(
    config.DATABASE_URL,
    convert_unicode=True
)

db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
))
Base = declarative_base(cls=BaseModel)
Base.query = db_session.query_property()


class IdMixin(object):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower() + 's'

    @classmethod
    def get(cls, id):
        return cls.query.filter(cls.id == id).first()

    pass


defcnt = 0


def ForeignMixin(name, target):
    global defcnt
    attr = name + '_id'
    obj = type('ForeignMixin_' + name, (object,),
               {attr: declared_attr(lambda cls: Column(Integer, ForeignKey(target.__tablename__ + '.id'))),
                name: declared_attr(lambda cls: relationship(target, primaryjoin=target.id == getattr(cls, attr)))})
    setattr(target, str(defcnt), declared_attr(lambda cls: relationship(obj)))
    defcnt += 1
    return obj
