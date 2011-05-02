#!/usr/bin/python

from splitter import splitter
import sys
from blast_parser import *


def read_blast(blast, filt, pp):
    f = open(blast)
    for l in f.xreadlines():
        if not l.startswith('#') and filt(l):
            pp(l)

def all_uniq_subjects(blast):
    subjects = set()
    subj_field = BlastFields.index('Subject id')
    read_blast(blast,
        lambda x : True,
        lambda x : subjects.add('>'+extract_blast_fields(x, subj_field)[0])
    )
    f = open(blast+'.csv', 'w')
    def pr(x):
        print >> f, x
    map(pr, subjects)
    return subjects

if __name__=='__main__':
    linecounter=0
    linethreshold=65535
    map(all_uniq_subjects, sys.argv[1:])

