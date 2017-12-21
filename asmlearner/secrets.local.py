SECRET_KEY = "${os.urandom(28).encode('hex')}"
DATABASE_HOST = 'localhost'
DATABASE_USERNAME = 'asmlearner'
DATABASE_PASSWORD = '${os.urandom(28).encode("hex")}'
DATABASE_DB = 'asmlearner'
CELERY_URL = '${celery_url}'
CELERY_QUEUE_NAME = 'asmlearner'
