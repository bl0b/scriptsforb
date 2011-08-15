#!/usr/bin/env python

from csv_parser import Csv
from optparse import OptionParser
import sys


def getopts(args):
    parser = OptionParser()
    parser.add_option("-r", "--reference", dest="ref", help="a reference file to match against", default=None)
    parser.add_option("-i", "--input", dest="inp", help="a file that you want cross-referenced", default=None)
    parser.add_option("-o", "--output", dest="outp", help="the name of the output file (will default to input+'.xref'", default=None)
    parser.add_option("--rk", "--refkey", dest="refkey", help="columns indices that define the cross-referencing key (reference-side)", default=None)
    parser.add_option("--rc", "--refcol", dest="refcol", help="columns indices in reference file that should be appended to rows of the input file", default=None)
    parser.add_option("--ik", "--inputkey", dest="inkey", help="columns indices that define the cross-referencing key (input-side, defaults to refkey)", default=None)
    (options, args) = parser.parse_args(args)

    fail = False

    if options.ref is None:
        print "You must provide a reference file"
        fail = True
    if options.inp is None:
        print "You must provide an input file"
        fail = True
    if options.outp is None:
        options.outp = (options.inp or '')+'.xref'
        print "No output filename provided. Using", options.outp
    if options.refkey is None:
        print "You must provide a comma-separated list of column indices (starting at 0!)"
        fail = True
    if options.inkey is None:
        print "No key specified for input file. Assuming the same as in reference file"
        options.inkey = options.refkey
    if len(args)>0:
        print "Trailing arguments in commandline:", ' '.join(args)
        fail=True
    if fail:
        print
        print "Errors were detected in command line. Aborting."
        print
        parser.parse_args(['-h'])
        sys.exit(1)
    options.refkey = tuple(map(int, options.refkey.split(',')))
    options.inkey = tuple(map(int, options.inkey.split(',')))
    options.refcol = tuple(map(int, options.refcol.split(',')))
    return options, args



def do_xref(ref, inp, outp, refk, ink, payload):
    R = Csv(ref)
    I = Csv(inp)
    out = file(outp, 'w')
    blacklist = set(['seg', 'signal-peptide'])
    ridx = R.make_index(refk, payload, blacklist)
    print "Using (%s) as cross-referencing key"%(','.join(R.headers[refk]))
    xref = [ '\t'.join(I.headers+R.headers[payload]) ]
    nomatch=set()
    for row in I.data:
        key = row[ink]
        if len(blacklist.intersection(key))>0 or key in nomatch:
            xref.append('\t'.join(row).strip())
            continue
        if key not in ridx:
            print "No match for (%s)"%(','.join(key))
            nomatch.add(key)
            xref.append('\t'.join(row).strip())
            continue
        matches = ridx[row[ink]]
        print len(matches), "match(es)"
        for m in matches:
            xref.append('\t'.join(row+m[payload]).strip())
    for x in xref:
        print >> out, x
    

if __name__=='__main__':
    options, args = getopts(sys.argv[1:])
    do_xref(options.ref, options.inp, options.outp, options.refkey, options.inkey, options.refcol)

