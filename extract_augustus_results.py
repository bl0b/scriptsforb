#!/usr/bin/env python
from parse_gff3 import parse_gff3
import fasta
import sys

if len(sys.argv) != 2:
    print "Usage: %s gff_file"
    sys.exit(0)

inf = sys.argv[1]
outdna = inf + '.dna.fas'
outprot = inf + '.prot.fas'
outgff = inf + '.gff3'

g = parse_gff3(sys.argv[1])

# First, extract DNA and protein fasta

for seq, outf in (('protein_seq', outprot), ('coding_seq', outdna)):
    f = fasta.Fasta()
    for x in g:
        f.add_seq(fasta.Sequence(x.name + ' ' + x[0].reference_sequence,
                                 getattr(x, seq)))
    f.save_to(outf)

# Now, output all GFF data.

outf = open(outgff, 'w')
print >> outf, "##gff-version\t3"
for p in (p for x in g for p in x):
    print >> outf, str(p)
