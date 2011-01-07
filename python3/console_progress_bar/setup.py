#!/usr/bin/env python3
#
#  Corey Goldberg - 2011
#


""" Setup script for console_progress_bar """


from distutils.core import setup


setup(
        name = 'console_progress_bar',
        version = '0.1.0',
        py_modules = ['console_progress_bar'],
        author = 'corey goldberg',
        author_email = 'corey@goldb.org',
        url = 'http://code.google.com/p/corey-projects/wiki/console_progress_bar',
        description = 'ascii command-line progress bar with percentage and elapsed time display',
        download_url = '',
        classifiers = [
            'Environment :: Console',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Topic :: Terminals',
            ]
     )
     
