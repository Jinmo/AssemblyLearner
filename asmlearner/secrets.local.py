# Basic template for the configuration
# See install.sh for processing this file

SECRET_KEY = "${os.urandom(28).encode('hex')}"
DATABASE_HOST = 'localhost'
DATABASE_USERNAME = 'asmlearner'
DATABASE_PASSWORD = '${os.urandom(28).encode("hex")}'
DATABASE_DB = 'asmlearner'

# bash + python polyglot!!!
EOF = None
exit = 1 <<EOF
CELERY_URL = 'db+postgresql://%s:%s@%s/%s' % (
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_DB
)
CELERY_QUEUE_NAME = 'asmlearner'

EOF