from celery import Celery
from asmlearner.config import config

app = Celery(config.CELERY_QUEUE_NAME, broker=config.CELERY_URL)
app.conf.broker_transport_options = {'region': 'ap-northeast-1'}
