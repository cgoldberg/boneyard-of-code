#!/usr/bin/env python
#
#  http://paste.pocoo.org/show/402065/ by Mark McMahon 2011
#

"""
Use pygments to output syntax highlighted PNG files of Python code
"""

import glob
import re
import sys
import os

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

PYGMENTS_STYLE = "pastie"
HIGHLIGHT_COLOR = "#ffdddd"


def main():
    highligth_marker = re.compile("\#\#\s*$")

    if sys.argv[1:]:
        path = sys.argv[1]
    else:
        path = "."

    for f in glob.glob(os.path.join(path, "*.py")):
        code = open(f).readlines()

        # collect the lines to be highlighted
        highlights = []
        for i, line in enumerate(code):
            line = line.rstrip()
            if highligth_marker.search(line):
                code[i] = highligth_marker.sub("", line)
                highlights.append(i + 1)
            else:
                code[i] = line

        data = highlight(
            "\n".join(code), PythonLexer(), ImageFormatter(
                font_size=24,
                style=PYGMENTS_STYLE,
                hl_lines=highlights,
                hl_color=HIGHLIGHT_COLOR))
        open(f + '.png', 'wb').write(data)


if __name__ == '__main__':
    main()