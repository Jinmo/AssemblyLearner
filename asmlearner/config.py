from os.path import dirname, join, realpath, abspath

PROJECT_DIR = abspath(join(dirname(realpath(__file__)), '..'))
DATABASE = join(PROJECT_DIR, 'db.db')


def randomkey(length):
    import random
    import string
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


# SECRET_KEY = 'lolthisissecretkeyforthisapp'
SECRET_KEY = randomkey(28)

CC_PATH = '/usr/bin/gcc'
OBJDUMP_PATH = '/usr/bin/objdump'
TRACER_PATH = join(PROJECT_DIR, 'asmlearner/bin/tracer')
INCLUDE_PATH = join(PROJECT_DIR, 'include')
