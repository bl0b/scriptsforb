#!/usr/bin/env python

from csv_parser import Csv
from optparse import OptionParser
import sys

"""Cross-reference [FIXME] results in a CSV file with [FIXME] results
in another CSV file"""

executable = True


def getopts(args):
    parser = OptionParser()
    parser.add_option("-r", "--reference", dest="ref",
                      help="a reference file to match against",
                      default=None)
    parser.add_option("-i", "--input", dest="inp",
                      help="a file that you want cross-referenced",
                      default=None)
    parser.add_option("-o", "--output", dest="outp",
                      help="the name of the output file (will default to " +
                           "input+'.xref'",
                      default=None)
    parser.add_option("--rk", "--refkey", dest="refkey",
                      help="columns indices that define the cross-referencing"
                      + " key (reference-side)", default=None)
    parser.add_option("--rc", "--refcol", dest="refcol",
                      help="columns indices in reference file that should be "
                      + "appended to rows of the input file", default=None)
    parser.add_option("--ik", "--inputkey", dest="inkey",
                      help="columns indices that define the cross-referencing"
                      + " key (input-side, defaults to refkey)", default=None)
    parser.add_option("-u", "--uniq", dest="uniq", action="store_true",
                      help="only output the unique cross-referenced payload "
                      + "entries", default=False)
    parser.add_option("-q", "--quiet", dest="quiet", action="store_true",
                      help="don't output every little detail", default=False)
    (options, args) = parser.parse_args(args)

    fail = False

    if options.ref is None:
        print "You must provide a reference file"
        fail = True
    if options.inp is None:
        print "You must provide an input file"
        fail = True
    if options.outp is None:
        options.outp = (options.inp or '') + '.xref'
        print "No output filename provided. Using", options.outp
    if options.refkey is None:
        print "You must provide a comma-separated list of column indices",
        print "(starting at 0!)"
        fail = True
    if options.inkey is None:
        print "No key specified for input file. Assuming the same as in",
        print "reference file"
        options.inkey = options.refkey
    if len(args) > 0:
        print "Trailing arguments in commandline:", ' '.join(args)
        fail = True
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


def xref_init(I, R, payload):
    return ['\t'.join(I.headers + R.headers[payload])]


def xref_add(xref, row, payload=Csv.Row([])):
    xref.append('\t'.join(row + payload).strip())


def uniq_init(I, R, payload):
    return set()


def uniq_add(xref, row, payload=Csv.Row([])):
    xref.add('\t'.join(payload))


def do_xref(ref, inp, outp, refk, ink, payload, uniq, quiet):
    R = Csv(ref)
    I = Csv(inp)
    out = outp == 'stdout' and sys.stdout or file(outp, 'w')
    blacklist = set(['seg', 'signal-peptide'])
    ridx = R.make_index(refk, payload, blacklist)
    if not quiet:
        print "Using (%s) as cross-referencing key" % (
            ','.join(R.headers[refk]))
    if uniq:
        xref = uniq_init(I, R, payload)
        add = uniq_add
    else:
        xref = xref_init(I, R, payload)
        add = xref_add
        #xref = [ '\t'.join(I.headers+R.headers[payload]) ]
    nomatch = set()
    for row in I.data:
        key = row[ink]
        if len(blacklist.intersection(key)) > 0 or key in nomatch:
            add(xref, row)
            #xref.append('\t'.join(row).strip())
            continue
        if key not in ridx:
            if not quiet:
                print "No match for (%s)" % (','.join(key))
            nomatch.add(key)
            add(xref, row)
            #xref.append('\t'.join(row).strip())
            continue
        matches = ridx[row[ink]]
        if not quiet:
            print len(matches), "match(es)"
        for m in matches:
            add(xref, row, m)
            #xref.append('\t'.join(row+m[payload]).strip())
    for x in xref:
        print >> out, x


if __name__ == '__main__':
    options, args = getopts(sys.argv[1:])
    do_xref(options.ref, options.inp, options.outp, options.refkey,
            options.inkey, options.refcol, options.uniq, options.quiet)
