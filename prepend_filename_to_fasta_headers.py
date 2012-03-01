#!/usr/bin/env python

from fasta import Fasta
import sys
import os

if len(sys.argv) == 1 or sys.argv[1] in ('-h', '--help'):
    print "Usage: %s fasta_file..." % sys.argv[0]
    sys.exit(0)

for filename in sys.argv[1:]:
    dirname, basename = os.path.split(filename)
    root, ext = os.path.splitext(basename)
    output = root + '-prefixed' + ext

    f = Fasta()

    try:
        f.read_from(filename)
    except IOError, ioe:
        print "Error:", str(ioe)
        continue

    for seq in f:
        seq.header = root + '_' + seq.header
    f.save_to(output)
