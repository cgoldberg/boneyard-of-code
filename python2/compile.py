#!/usr/bin/env python
# Corey Goldberg

from distutils.core import setup
import py2exe
import sys

if len(sys.argv) == 2:
    entry_point = sys.argv[1]
    sys.argv.pop()
    sys.argv.append('py2exe')
    sys.argv.append('-q')
else:
    print 'usage: compile.py <python_script>\n'
    raw_input('press ENTER to exit...')
    sys.exit(1)

opts = {
    'py2exe': {
        'compressed': 1,
        'optimize': 2,
        'bundle_files': 1
    }
}

setup(console=[entry_point], options=opts, zipfile=None)
