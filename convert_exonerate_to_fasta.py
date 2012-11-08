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
    ts_remove = set(['.', 'a', 'c', 't', 'g', '{', '}'])
    pred_ts = lambda x: x not in ts_remove
    suffix = '_STRIPPED'
else:
    pred_a = lambda x: True
    suffix = ''


for filename in args:
    e = Exonerate(filename)
    out = open(filename + suffix + '.fas', 'w')
    for q in e.queries:
        tseq = ''.join(ts
                       for qp, tp, ts, a
                        in q.iterate(pred_a=pred_a, pred_ts=pred_ts))
        s = Sequence(q.Query.split(' ')[0] + '_' + q.Target
                     + ('#' in q.alignment and suffix or ''),
                     tseq.replace('-', 'N'))
        print >> out, s
