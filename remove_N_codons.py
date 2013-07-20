#!/usr/bin/env python

import sys
import os
import fasta

splitext = os.path.splitext

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        f = fasta.Fasta()
        f.read_from(filename)
        for s in f:
            s.sequence.replace('NNN', '')
        basename, ext = splitext(filename)
        f.save_to(basename + '_N_removed' + ext)
