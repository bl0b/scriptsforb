#!/usr/bin/env python
from parse_gff3 import parse_gff3
import fasta
import sys

if len(sys.argv) != 3:
    print "Usage: %s gff_file output_fasta_file"
    sys.exit(0)

g = parse_gff3(sys.argv[1])
f = fasta.Fasta()
for x in g:
    f.add_seq(fasta.Sequence(x.name + ' ' + x[0].sequence_name, x.protein_seq))
f.save_to(sys.argv[2])
