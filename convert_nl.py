#!/usr/bin/env python

import os
import sys
import re
from optparse import OptionParser


op = OptionParser()
op.add_option("-u", "--to-unix", dest="u",
              help="Windows/Mac -> Unix",
              action='store_true', default=False)
op.add_option("-m", "--to-mac", dest="m",
              help="Windows/Unix -> Mac",
              action='store_true', default=False)
op.add_option("-w", "--to-windows", dest="w",
              help="Unix/Mac -> Windows",
              action='store_true', default=False)

op.usage += """ [<file-or-directory> ...]

Forcefully converts newlines as required.
Specify individual files or directories to process all files therein.

Each file will be backupped with a .bak extension.
"""

mac_re = re.compile('\r(?!\n)')
unix_re = re.compile('(?<!\r)\n')
win_re = re.compile('\r\n')

transform = {
# target:
#    Unix   Mac    Windows
    (True,  False, False): ((win_re, '\n'), (mac_re, '\n')),
    (False, True,  False): ((win_re, '\r'), (unix_re, '\r')),
    (False, False, True): ((unix_re, '\r\n'), (mac_re, '\r\n')),
}


def convert(u, m, w, data):
    for expr, repl in transform[u, m, w]:
        data = expr.sub(repl, data)
    return data


def iter_args(args):
    for arg in args:
        if os.path.isfile(arg):
            yield arg
        elif os.path.isdir(arg):
            for sub in iter_args(os.path.join(arg, f)
                                 for f in os.listdir(arg)):
                yield sub


if __name__ == '__main__':
    opts, args = op.parse_args(sys.argv[1:])

    if (opts.w + opts.u + opts.m) != 1:
        print "Please specify exactly one of -u, -w, -m."
        print
        op.parse_args(["-h"])
        sys.exit(-1)

    if len(args) == 0:
        print "Please specify at least one file or directory."
        print
        op.parse_args(["-h"])
        sys.exit(-1)

    for f in iter_args(args):
        data = open(f).read()
        open(f + '.bak', 'wb').write(data)
        open(f, 'wb').write(convert(opts.u, opts.m, opts.w, data))
