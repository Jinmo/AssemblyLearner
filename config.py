from os.path import dirname, join


CURPATH = dirname(realpath(__file__))
DATABASE = join(CURPATH, 'db.db')

print os.path.realpath(__file__)