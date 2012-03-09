from csv_parser import Csv
import sys

inf = sys.argv[1]
outf = inputf + '.transposed'

print >> open(outf, 'w'), '\n'.join(','.join(d) for d in Csv(inf, ',').data)
