#!/usr/bin/env python

import parse_gff2
import parse_gff3
import fasta
import sys
from optparse import OptionParser
from itertools import imap

if __name__ == '__main__':
    opts = OptionParser()
    opts.add_option("-f", "--fasta", dest="fas",
                    help="The reference sequences to extract the features"
                         + " from",
                    default=None)
    opts.add_option("-2", "--gff2", dest="gff2",
                    help="The GFF2 file describing the features to extract",
                    default=None)
    opts.add_option("-3", "--gff3", dest="gff3",
                    help="The GFF3 file describing the features to extract",
                    default=None)
    opts.add_option("-o", "--output", dest="output",
                    help="The output filename (default: stdout)",
                    default=None)

    opts.usage += ("\n\nThis program extracts the features described in the"
                   + " GFF file from the fasta file AS THEY ARE, without doing"
                   + " any reverse complement or whatever.")

    o, args = opts.parse_args(sys.argv[1:])

    if len(args) > 0:
        print "Trailing arguments", " ".join(args)
        sys.exit(1)

    if o.gff2 is not None and o.gff3 is not None:
        print "Specify either gff2 or gff3 but not both."
        sys.exit(1)

    if o.fas is None:
        print "Specify the fasta database file."
        sys.exit(1)

    if o.output is None:
        o.output = sys.stdout
    else:
        o.output = file(o.output, "w")

    fas = fasta.Fasta()
    fas.read_from(o.fas)

    if o.gff2:
        gff = parse_gff2.parse_gff2(o.gff2)
    else:
        gff = parse_gff3.parse_gff3(o.gff3)

    try:
        l = [fasta.Sequence(
                g.reference_sequence + ' ' + g.start + ' ' + g.stop
                + ' ' + g.strand,
                fas[g.reference_sequence].sequence[int(g.start)
                                                   - 1:int(g.stop)])
         for g in gff]
        print >> o.output, '\n'.join(imap(str, l))
    except KeyError, ke:
        print "Sequence was not found in fasta file :", str(ke)
