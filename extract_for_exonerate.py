#!/usr/bin/env python
import fasta
import os
import sys

fcount = 0
ftotal = 0


def extract(filename):
    global fcount, ftotal
    fcount += 1
    print "\r%i/%i" % (fcount, ftotal),
    exti = filename.rfind('.')
    ext = filename[exti:]
    path, query = os.path.split(filename[:exti])
    fhits = fasta.read_from(filename)
    if query in fhits:
        fquery = fasta.Fasta()
        fquery.add_seq(fhits[query])
        fhits.remove(query)
        fhits.save_to(os.path.join(path, query + '-hits' + ext))
        fquery.save_to(os.path.join(path, query + '-query' + ext))


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] in ('-h', '--help'):
        print "Usage:"
        print sys.argv[0], "[-h,--help] [-w fasta_width] fasta_file..."
        sys.exit(0)
    if args[0] == '-w':
        fasta.WIDTH = int(args[1])
        args = args[2:]
    print "Extracting queries from", len(args), "files..."
    ftotal = len(args)
    map(extract, args)
