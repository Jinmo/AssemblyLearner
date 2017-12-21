import os
import asmlearner.secrets as secrets
import urllib2


def generate_random_key(length):
    import random
    import string
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


class Config(object):
    PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
    TRACER_PATH = os.path.join(PROJECT_DIR, 'asmlearner', 'bin', 'tracer')
    INCLUDE_PATH = os.path.join(PROJECT_DIR, 'include')
    SNIPPET_PATH = os.path.join(PROJECT_DIR, 'data', 'snippet')

    CC_PATH = '/usr/bin/gcc'
    OBJDUMP_PATH = '/usr/bin/objdump'
    DATABASE_URL = 'postgresql+psycopg2://{username}:{password}@{host}/{db}'.format(
        host=secrets.DATABASE_HOST,
        username=secrets.DATABASE_USERNAME,
        password=urllib2.quote(secrets.DATABASE_PASSWORD),
        db=secrets.DATABASE_DB
    )

    CELERY_URL = secrets.CELERY_URL
    CELERY_QUEUE_NAME = secrets.CELERY_QUEUE_NAME
    SECRET_KEY = secrets.SECRET_KEY


config = Config()
