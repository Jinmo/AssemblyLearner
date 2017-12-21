#!/usr/bin/env python

from asmlearner.tasks import app as celery_app

celery_app.add_consumer()