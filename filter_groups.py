#!/usr/bin/env python

from itertools import chain, imap
import os, sys

# attempt at creating a trie-like index of the entries in first column of csv file.

class Trie(dict):
    """Quick indexing of many strings in order to find common prefixes"""
    def __init__(self):
        dict.__init__(self)
        self.payload = []
    def add(self, s, p):
        """Add a string to the index, associated with a payload"""
        if len(s)==0:
            return
        if s[0] not in self:
            t = Trie()
            self[s[0]] = t
        if len(s)>1:
            self[s[0]].add(s[1:], p)
        else:
            self[s[0]].payload.append(p)
    def __str__(self):
        return str(self.payload)+":"+dict.__str__(self)
    def __repr__(self):
        return repr(self.payload)+":"+dict.__repr__(self)

    def list_entries(self):
        """List ALL entries"""
        ret_parts = []
        for letter, trie in self.iteritems():
            #print letter, trie
            if trie.payload:
                ret_parts += [ [letter] ]
            ret_parts += [ [letter+e for e in trie.list_entries()] ]
        #print list(chain(*ret_parts))
        return list(chain(*ret_parts))

    def list_prefixes(self):
        """List all entries that are prefixes of longer strings"""
        ret_parts = []
        for letter, trie in ((l, t) for l, t in self.iteritems() if len(t)>0):
            #print letter, trie
            if trie.payload:
                ret_parts += [ [letter] ]
            ret_parts += [ [letter+e for e in trie.list_prefixes()] ]
        #print list(chain(*ret_parts))
        return list(chain(*ret_parts))

    def get_subtrie(self, s):
        """Helper to get the subtree (subtrie) of a given prefix"""
        t = self
        i = 0
        while i<len(s):
            t = t[s[i]]
            i += 1
        return t

    def list_suffixes(self, s): # FIXME : suffixes should mean only the substrings, not the concatenated entries (see the map() at the end)
        """List all strings starting with s (return full entries, not only suffixes)"""
        #print "finding suffixes of", s
        t = self.get_subtrie(s)
        return map(lambda x : s+x, t.list_entries())

    def __call__(self, s):
        """Get the payload associated to entry s"""
        return self.get_subtrie(s).payload



def looks_like_an_alignment(l):
    w = l.split('\t')
    return len(w)>2 and w[2] not in ('', 'EMPTY')


def open_file(fn):
    lineiter = enumerate(open(fn).xreadlines())
    zero, headers = lineiter.next()
    return lineiter, headers



def save_to_file(inputfilename, loi, goi):
    lineiter, headers = open_file(inputfilename)
    f = open(inputfilename+'.filtered.csv', 'w')
    f.write(headers)
    for i, l in lineiter:
        #print ' line', i, l[:50], "\r"
        if i in loi or looks_like_an_alignment(l): # always output something that looks like an alignment row
            #print "output <", l[:50], "...> to", loi[i], '                     \r',
            f.write(l)
    print "output saved to", f.name






def save_to_files(inputfilename, loi, goi):
    lineiter, headers = open_file(inputfilename)
    headers.strip()
    try:
        os.makedirs(inputfilename+'.GOI')
    except IOError, ioe:
        pass
    except OSError, ioe:
        pass
    def select_file(tag, mode='a'):
        """Simply open a file (default to append mode) for one output, because it's probably unsage to open all output files at once."""
        return open(inputfilename+'.GOI/'+tag+'.csv', mode)

    for g in goi.iterkeys():
        print >> select_file(g, 'w'), headers
    for i, l in lineiter:
        #print ' line', i, l[:50], "\r"
        if i in loi:
            l.strip()
            #print "output <", l[:50], "...> to", loi[i], '                     \r',
            print >> select_file(loi[i]), l




if __name__=='__main__':
    #words = ('foobar', 'bouba', 'foobarbaz', 'foobaz')
    #words = ('aa', 'ab', 'ba')

    if len(sys.argv)==1 or sys.argv[1] in ('-h', '--help'):
        print "%s: filter groups of results from a tab-separated csv file."%sys.argv[0]
        print "Usage: %s csv_file"%sys.argv[0]
        print "Outputs the results in 'csv_file.filtered.csv'."
        sys.exit(0)

    inputfilename = sys.argv[1]

    #
    # First pass : make index
    #
    lineiter, headers = open_file(inputfilename)
    words = ((l[0:l.find('\t')], i) for (i, l) in lineiter)
    t=Trie()
    map(lambda x: t.add(*x), words)
    #print headers
    #print words
    print "entry count:", len(t.list_entries())
    prefixes = t.list_prefixes()
    #print "prefix count:", len(prefixes)
    #print "suffixes(%s):"%prefixes[0], t.list_suffixes(prefixes[0])
    #print "payload of", prefixes[0], t(prefixes[0])

    #
    # Second pass : determine groups of interest
    #
    groupof = {} # name -> group-name
    group = {} # group-name -> list of names
    for p in prefixes:
        groupof[p] = p
        group[p] = set(p)
        for s in t.list_suffixes(p):
            groupof[s] = p
            group[p].add(s)

    groups_of_interest = set()
    lineiter, headers = open_file(inputfilename)
    words = ((l, l.split('\t')[:3], i) for (i, l) in lineiter)
    for l, w, i in words:
        if looks_like_an_alignment(l) and w[0] in groupof:
            #print "seeing", w[2][:20], "makes me think group", groupof[w[0]], "is of interest"
            groups_of_interest.add(groupof[w[0]])
    print "out of", len(prefixes), "possible groups, found", len(groups_of_interest), "distinct groups of interest"

    #
    # Intermission : strip groups not of interest and associate line numbers with groups
    #
    goi = {} # group of interest, short version
    for p in groups_of_interest:
        goi[p] = list(chain(*map(lambda x: t(x), group[p])))

    loi = {} # lines of interest
    for tag, lines in goi.iteritems():
        for l in lines:
            loi[l] = tag

    #print goi
    #print loi

    #
    # Third pass : output to files
    #
    save_to_file(inputfilename, loi, goi)
    #save_to_files(inputfilename, loi, goi)

    sys.exit(0)




