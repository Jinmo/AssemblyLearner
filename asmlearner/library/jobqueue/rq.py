import os
import sys

from rq.cli import main

def cli():
    py = os.path.realpath(__file__)
    pydir = os.path.dirname(py)
    os.chdir(pydir)

    if len(sys.argv) == 1:
        sys.argv.append('worker')

    sys.exit(main())
