#!/usr/bin/env python

from optparse import OptionParser
import sys


def getopts(args):
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="inp", help="the name of the input file", default=None)
    parser.add_option("-o", "--output", dest="outp", help="the name of the output file", default=None)
    parser.add_option("-s", "--start", dest="slen", help="count of characters to keep from left (start) of header string (initial '>' not included)", default=None)
    parser.add_option("-e", "--end", dest="elen", help="count of characters to keep from right (end) of header string (initial '>' not included)", default=None)
    (options, args) = parser.parse_args(args)

    fail = False

    if options.inp is None:
        print "You must provide an input file"
        fail = True
    if options.outp is None:
        print "You must provide an output file"
        fail = True
    if options.outp==options.inp:
        print "You must provide an output filename DIFFERENT from the input filename"
        fail = True
    if options.slen is None or options.elen is None:
        print "You must provide both -s [num] and -e [num] options"
        fail = True
    if len(args)>0:
        print "Trailing arguments in commandline:", ' '.join(args)
        fail=True
    if fail:
        print
        print "Errors were detected in command line. Aborting."
        print
        parser.parse_args(['-h'])
        sys.exit(1)
    options.elen = int(options.elen)
    options.slen = int(options.slen)
    return options, args



def rewrite_fasta(fin, fout, header_shrinker):
    for l in fin.xreadlines():
        l=l.strip()
        if len(l)>0 and l[0]=='>':
            fout.write('>')
            print >> fout, header_shrinker(l[1:])
        else:
            print >> fout, l


if __name__=='__main__':
    options, args = getopts(sys.argv[1:])

    fin = open(options.inp, 'r')
    fout = open(options.outp, 'w')

    totlen = options.slen+options.elen
    def shrink_by_charcount(l):
        if len(l)>totlen:
            return l[:options.slen]+l[-options.elen:]
        else:
            return l

    rewrite_fasta(fin, fout, shrink_by_charcount)

