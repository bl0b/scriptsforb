#!/usr/bin/python

from splitter import splitter
import sys, re
from blast_parser import *

quit_skipping = "start  len      tm     gc%   any    3' seq"
resume_skipping = "Statistics"

fint_ = '[0-9]+'
fint = '('+fint_+')'
ffloat = '('+fint_+r'\.'+fint_+')'
fspace = ' +'
LR_COMMON = fspace.join([fint, fint, ffloat, ffloat, ffloat, ffloat, '([tcagACGT]+)'])
LEFT_RE = re.compile(fint+' +LEFT PRIMER +'+LR_COMMON)
RIGHT_RE = re.compile('RIGHT PRIMER +'+LR_COMMON)
PRODUCT_SIZE_RE = re.compile('PRODUCT SIZE: '+fint+', PAIR ANY COMPL: '+ffloat+", PAIR 3' COMPL: "+ffloat)

lr_fields = ( 'start', 'len', 'tm', 'gc%', 'any', "3'", 'seq' )
lr_types = ( int, int, float, float, float, float, str)

def match2type(fields):
    return [lr_types[i](fields[i]) for i in xrange(len(fields))]

class primer3(object):
    def __init__(self):
        self.num = None
        self.left = None
        self.right = None
        self.product_size = None
        self.pair_any_compl = None
        self.pair_3_compl = None
    def add_line(self, l):
        try:
            if self.left is None:
                #print "left>", l
                fields = LEFT_RE.match(l).groups()
                self.num = int(fields[0])
                self.left = dict(zip(lr_fields, match2type(fields[1:])))
            elif self.right is None:
                #print "right>", l
                fields = RIGHT_RE.match(l).groups()
                self.right = dict(zip(lr_fields, match2type(fields)))
            elif self.product_size is None:
                #print "misc>", l
                self.product_size, self.pair_any_compl, self.pair_3_compl = PRODUCT_SIZE_RE.match(l).groups()
            return self.product_size is not None
        except Exception, e:
            print "Couldn't parse file around line :"
            print l
            sys.exit(0)
    def __str__(self):
        return '<primer3 #%i left=%s right=%s>'%(self.num, self.left['seq'], self.right['seq'])
    def __repr__(self):
        return '<primer3 #%i left=%s right=%s>'%(self.num, self.left['seq'], self.right['seq'])


def primer3_parse(f):
    ret = [ None ]
    if type(f) is str:
        f = open(f)
    skipping = True
    get_header = False
    header = [ 'label' ]
    buf = f.read()
    sep=''
    if '\r' in buf:
        sep = '\r'
    if '\n' in buf:
        sep += '\n'
    lines = buf.split(sep)
    for l in lines:
        l = l.strip()
        if not l:
            continue
        if skipping:
            if l==quit_skipping:
                skipping = False
            continue
        elif l==resume_skipping:
            skipping = True
            continue
        if ret[-1] is None:
            ret[-1] = primer3()
        if ret[-1].add_line(l):
            ret.append(None)
    if ret[-1] is None:
        ret.pop()
    return ret




def primer_to_fasta(num, lr, pfields):
    return '>%i %s %i\n%s\n'%(num, lr, pfields['start'], pfields['seq'])



if __name__=='__main__':
    for inputfile in sys.argv[1:]:
        inputfile = sys.argv[1]
        test = primer3_parse(inputfile)
        print >> open(inputfile+'.fasta', 'w'), '\n'.join(map(lambda p: primer_to_fasta(p.num, 'left', p.left)+primer_to_fasta(p.num, 'right', p.right), test))

