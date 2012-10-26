#!/usr/bin/env python
from parse_exonerate import Exonerate
import sys
from fasta import Sequence

args = sys.argv[1:]

if '-h' in args or '--help' in args:
    print "Usage: %s [-s] exonerate_files..." % sys.argv[0]
    print
    print "  -s   strip unaligned indels from outputs"
    print "       (hash signs in alignment)"
    sys.exit(0)

if args[0] == '-s':
    args = args[1:]
    pred_a = lambda x: x != '#'
else:
    pred_a = lambda x: True


for filename in args:
    e = Exonerate(filename)
    out = open(filename + '.fas', 'w')
    for q in e.queries:
        tseq = ''.join(ts
                       for qp, tp, ts, a
                        in q.iterate(pred_a=pred_a))
        s = Sequence(q.Query.split(' ')[0] + '_' + q.Target
                     + ('#' in q.alignment and '_STRIPPED' or ''),
                     tseq.replace('-', 'N'))
        print >> out, s
