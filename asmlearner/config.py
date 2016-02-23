from os.path import dirname, join, realpath, abspath

PROJECT_DIR = abspath(join(dirname(realpath(__file__)), '..'))
DATABASE = join(PROJECT_DIR, 'db.db')

SECRET_KEY = 'lolthisissecretkeyforthisapp'

CC_PATH = '/usr/bin/gcc'
OBJDUMP_PATH = '/usr/bin/objdump'
TRACER_PATH = join(PROJECT_DIR, 'asmlearner/bin/tracer')
INCLUDE_PATH = join(PROJECT_DIR, 'include')
