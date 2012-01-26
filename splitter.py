#!/usr/bin/env python

import sys

class splitter(object):
    def __init__(self, slice_size):
        self.slice_size = slice_size

    def open_next_file(self):
        self.output_len=0
        self.output_index+=1
        self.output_file = open("%s.%i"%(self.filename, self.output_index), 'w')

    def output_line(self, l):
        if self.output_len>=self.slice_size:
            self.open_next_file()
        print >> self.output_file, l.strip()
        self.output_len+=1

    def __call__(self, filename):
        self.filename = filename
        self.output_len=self.slice_size
        self.output_index = 0
        map(self.output_line, open(filename).xreadlines())


def main():
    ssz = 0
    fnames = []
    if len(sys.argv)>2 and sys.argv[1]=="-s":
        ssz = int(sys.argv[2])
        fnames = sys.argv[3:]
    else:
        ssz = 65535
        fnames = sys.argv[1:]
    map(splitter(ssz), fnames)

if __name__=='__main__':
    main()

