#!/usr/bin/env python
import os
import sys

"""Modify Fasta headers in *.fasta files to include the raw filename
(without the extension)"""

if __name__ == '__main__':

    if not sys.argv[1:]:
        print "Please provide one or more directories in which there are",
        print "fasta files to be processed."
        sys.exit(-1)

    def update_headers(d):
        fastas = filter(lambda f: f.endswith('.fasta'), os.listdir(d))
        for f in fastas:
            base = os.path.join(d, f)
            if not os.path.exists(base + '.bak'):
                open(base + '.bak', 'w').write(open(base).read())
            src = open(base)
            src.readline()  # skip header
            data = src.read()
            src.close()
            dest = open(base, 'w')
            print >> dest, '>' + f[:-6]
            dest.write(data)

    map(update_headers, sys.argv[1:])
