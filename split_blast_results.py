#!/usr/bin/env python

from blast_parser import parse_file
import os, sys

if __name__=='__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print "Usage: %s [-h|--help] [-o|--output dirname] blast_result_file"
        sys.exit(0)

    inp = sys.argv[-1]
    output = ""
    if '-o' in sys.argv:
        output = sys.argv[sys.argv.index('-o')+1]
    elif '--output' in sys.argv:
        output = sys.argv[sys.argv.index('--output')+1]
    else:
        ext_index = inp.rfind('.')
        if ext_index==-1:
            output = inp+'_results'
        else:
            output = inp[:ext_index]
    try:
        os.makedirs(output)
    except OSError, ioe:
        pass

    results = parse_file(sys.argv[1])
    for r in results:
        print >> open(output+'/'+r.query+'.txt', 'w'), r
