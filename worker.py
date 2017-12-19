#!/usr/bin/env python

import os

os.system('celery -A asmlearner.tasks worker')