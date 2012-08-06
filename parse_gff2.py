class Feature(object):

    def __init__(self, reference_sequence, source, method, start, stop, score,
                 strand, phase, group):
        self.group = group
        self.reference_sequence = reference_sequence
        self.source = source
        self.method = method
        self.start = start
        self.stop = stop
        self.score = score
        self.strand = strand
        self.phase = phase

    def __str__(self):
        return '\t'.join([self.reference_sequence, self.source, self.method,
                          self.start, self.stop, self.score, self.strand,
                          self.phase, self.group])

    __repr__ = __str__


def parse_gff2(gff_file):
    predfeatures = []
    mode = ''
    if type(gff_file) is str:
        gff_file = open(gff_file)

    for l in gff_file:  # .xreadlines():
        l = l.strip()
        if not l.startswith('#'):
            X = l.split('\t')
            if len(X) == 8:  # no group
                X.append("")
            group = '\t'.join(X[8:])
            X = X[:8] + [group]
            #print X
            predfeatures.append(Feature(*X))
    return predfeatures
