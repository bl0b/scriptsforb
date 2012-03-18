#!/usr/bin/env python

from query_primer3 import query_primer3
import fasta
import sys
import re
import os

if len(sys.argv) < 2:
    print "Usage: %s multi_fasta PRIMER3_ARG=VALUE..."

mfas = fasta.read_from(sys.argv[1])
primer3args = sys.argv[2:]

bad_chr = re.compile("[^a-zA-Z0-9_-]")

basedir, basename = os.path.split(sys.argv[1])

for i, s in enumerate(mfas):
    out = os.path.join(basedir, bad_chr.sub('_', s.header) + '.primer3')
    print '[%i/%i]' % (1 + i, len(mfas)), "Querying", s.header
    query_primer3(['SEQUENCE=' + s.sequence, '-o', out] + primer3args)
