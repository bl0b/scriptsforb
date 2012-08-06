#!/usr/bin/env python
from parse_exonerate import Exonerate
import sys
from fasta import Sequence

for filename in sys.argv[1:]:
    e = Exonerate(filename)
    out = open(filename + '.fas', 'w')
    for q in e.queries:
        s = Sequence(q.Query.split(' ')[0] + '_' + q.Target,
                     q.target_seq.replace('-', 'N'))
        print >> out, s
