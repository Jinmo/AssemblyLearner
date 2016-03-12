#!/usr/bin/python3

import os
import sys

from rq.cli import main

if __name__ == '__main__':
    py = os.path.realpath(__file__)
    pydir = os.path.dirname(py)
    os.chdir(pydir)

    if len(sys.argv) == 1:
        sys.argv.append('worker')

    sys.exit(main())
