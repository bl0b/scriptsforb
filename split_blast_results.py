#!/usr/bin/env python

from blast_parser import parse_file
import os
import sys
from optparse import OptionParser


def getopts(args):
    parser = OptionParser()
    parser.add_option("-o", "--output", dest="output_dir",
                      help="force the output directory.",
                      default=None)
    parser.add_option("-F", "--format", dest="format_string",
                      help="format result rows with this string. Delimit field"
                           + " names or indices with {}.",
                      default=None)
    parser.add_option("-H", "--header-format", dest="header_format_string",
                      help="format headers with this string. Delimit header na"
                           + "mes (Version, Query, Database,Fields) with {}.",
                      default=None)
    parser.add_option("-f", "--fields", dest="field_list",
                      help="output only this comma-delimited selection of "
                           + "fields in result rows.",
                      default=None)
    parser.add_option("-n", "--no-header", dest="output_headers",
                      action="store_false",
                      help="don't dump result headers in output files.",
                      default=True)

    (options, args) = parser.parse_args(args)

    fail = False

    if len(args) != 1:
        print "You must specify exactly ONE input file"
        print
        parser.parse_args(['-h'])
        sys.exit(1)

    if options.field_list is not None:
        options.field_list = map(str.strip, options.field_list.split(","))

    if options.output_dir is None:
        ext_index = args[0].rfind('.')
        if ext_index == -1:
            options.output_dir = args[0] + '_results'
        else:
            options.output_dir = args[0][:ext_index]

    return options, args[0]


def main(args):
    options, inputfile = getopts(sys.argv[1:])

    results = parse_file(inputfile)

    try:
        os.makedirs(options.output_dir)
    except OSError, ioe:
        pass

    def outputfile(q):
        q = q.replace('/', '~')
        return open(options.output_dir + '/' + q + '.txt', 'w')

    for r in results:
        print >> outputfile(r.query), r.format(options.header_format_string
                                               or options.output_headers,
                                               options.format_string
                                               or options.field_list)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
