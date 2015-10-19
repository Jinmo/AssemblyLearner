from os.path import dirname, join, realpath, abspath

PROJECT_DIR = abspath(join(dirname(realpath(__file__)), '..'))
DATABASE = join(PROJECT_DIR, 'db.db')
