

class Csv(object):
    class Row(tuple):
        def __init__(self, a):
            tuple.__init__(self, (x.strip() for x in a))
        def __getitem__(self, x):
            if type(x) in (tuple, list, set):
                return Csv.Row((tuple.__getitem__(self, field) for field in x))
            else:
                return tuple.__getitem__(self, x)
    def __init__(self, filename, sep='\t'):
        f = open(filename)
        data = [ Csv.Row(l.split(sep)) for l in f.xreadlines() ]
        self.headers = Csv.Row((x.strip() for x in data[0]))
        self.data = data[1:]
    def make_index(self, columns, payload=None, blacklist=set()):
        ret = {}
        for row in self.data:
            key = row[columns]
            if len(blacklist.intersection(key))>0:
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



if __name__=='__main__':
    from sys import argv
    csv = Csv(argv[1])
    print csv.headers
    idx = csv.make_index((4,5), (0,), set(['seg', 'signal-peptide']))
    #print '\n'.join(map(str, idx.keys()))
    hist={}
    for k,v in idx.iteritems():
        #print "%40s %i"%(str(k), len(v))
        if len(v) in hist:
            hist[len(v)]+=1
        else:
            hist[len(v)]=1
        if len(v)>100:
            print len(v), k
    for k in sorted(hist.keys()):
        print k, hist[k]

