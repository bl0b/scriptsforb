import sys

"""Module to parse CSV files"""

executable = False


def parse_csv(filename, sep=','):
    f = open(filename)
    entries = []
    IN_STRING = False
    for l in f.xreadlines():
        l = l.strip()
        row = ['']
        for c in l:
            if c == sep and not IN_STRING:
                row.append('')
            elif c == '"' and IN_STRING:
                IN_STRING = False
            elif c == '"' and not IN_STRING:
                IN_STRING = True
            else:
                row[-1] += c
        entries.append(row)
    return entries


class Csv(object):
    class Row(tuple):
        def __init__(self, a):
            tuple.__init__(self, (x.strip() for x in a))

        def __getitem__(self, x):
            if type(x) in (tuple, list, set):
                try:
                    return Csv.Row((tuple.__getitem__(self, field)
                                    for field in x))
                except IndexError, ie:
                    print "Row is too short for ", x, ':', self
                    print "Aborting."
                    sys.exit(-1)
            else:
                return tuple.__getitem__(self, x)

    def __init__(self, filename, sep='\t', headers=True):
        f = open(filename)
        data = parse_csv(filename, sep)
        #[Csv.Row(l.strip().split(sep)) for l in f.xreadlines()]
        if headers:
            self.headers = Csv.Row((x.strip() for x in data[0]))
            self.data = data[1:]
        else:
            self.headers = Csv.Row([])
            self.data = data

    def make_index(self, columns, payload=None, blacklist=set()):
        ret = {}
        for row in self.data:
            key = row[columns]
            if len(blacklist.intersection(key)) > 0:
                continue
            if payload is None:
                r = row
            else:
                r = row[payload]
            if key in ret:
                ret[key].add(r)
            else:
                ret[key] = set([r])
        return ret


if __name__ == '__main__':
    from sys import argv
    csv = Csv(argv[1])
    print csv.headers
    idx = csv.make_index((4, 5), (0,), set(['seg', 'signal-peptide']))
    #print '\n'.join(map(str, idx.keys()))
    hist = {}
    for k, v in idx.iteritems():
        #print "%40s %i"%(str(k), len(v))
        if len(v) in hist:
            hist[len(v)] += 1
        else:
            hist[len(v)] = 1
        if len(v) > 100:
            print len(v), k
    for k in sorted(hist.keys()):
        print k, hist[k]
