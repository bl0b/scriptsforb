#!/usr/bin/env python

import os, sys

if not sys.argv[1:]:
    print "Please provide one or more directories in whicht here are fasta filest o be processed."
    sys.exit(-1)

def update_headers(d):
    fastas = filter(lambda f: f.endswith('.fasta'), os.listdir(d))
    for f in fastas:
        base = os.path.join(d, f)
        if not os.path.exists(base+'.bak'):
            open(base+'.bak', 'w').write(open(base).read())
        src = open(base)
        src.readline()  # skip header
        data = src.read()
        src.close()
        dest = open(base, 'w')
        print >> dest, '>'+f[:-6]
        dest.write(data)

map(update_headers, sys.argv[1:])

