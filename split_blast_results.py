#!/usr/bin/env python

from blast_parser import parse_file
import os, sys
from optparse import OptionParser

def getopts(args):
    parser = OptionParser()
    parser.add_option("-o", "--output", dest="outp", help="force the output directory.", default=None)
    parser.add_option("-f", "--format", dest="format_string", help="format result rows with this string. Delimit field names or indices with {}.", default=None)
    parser.add_option("-F", "--fields", dest="field_list", help="output only this comma-delimited selection of fields in result rows.", default=None)
    parser.add_option("-n", "--no-header", dest="output_headers", action="store_false", help="dump result headers in output files.", default=True)
    (options, args) = parser.parse_args(args)

    fail = False

    if len(args)!=1:
        print "You must specify exactly ONE input file"
        print
        parser.parse_args(['-h'])
        sys.exit(1)

    if options.field_list is not None:
        options.field_list = map(str.strip, options.field_list.split(","))

    if options.outp is None:
        ext_index = args[0].rfind('.')
        if ext_index==-1:
            options.outp = args[0]+'_results'
        else:
            options.outp = args[0][:ext_index]

    return options, args[0]



def main(args):
    options, inputfile = getopts(sys.argv[1:])

    results = parse_file(inputfile)

    try:
        os.makedirs(options.outp)
    except OSError, ioe:
        pass

    def outputfile(q):
        return open(options.outp+'/'+q+'.txt', 'w')

    for r in results:
        print >> outputfile(r.query), r.format(options.output_headers, options.format_string or options.field_list)

    return 0



if __name__=='__main__':
    sys.exit(main(sys.argv))

    # obsolete chunk
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
        print >> open(output+'/'+r.query+'.txt', 'w'), r.format(False, ">{Subject id}")
