#!/usr/bin/env python3
#
#  Copyright (c) 20?? Corey Goldberg (http://goldb.org)
#


""" setup/install script for sample-module """



from distutils.core import setup



setup(
        name = 'example-module',
        version = '0.1.0',
        description = 'this is an example module',
        author = 'Corey Goldberg',
        author_email = 'corey@goldb.org',
        py_modules = ['example-module'],
     )
     
