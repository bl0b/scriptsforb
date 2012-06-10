class PredictedRegion(object):

    def __init__(self, reference_sequence, source, feature, start, stop, score,
                 strand, frame, attributes):
        self.ID = None
        self.Parent = None
        for attstr in attributes.split(';'):
            setattr(self, *attstr.split("="))
        self.reference_sequence = reference_sequence
        self.source = source
        self.feature = feature
        self.start = start
        self.stop = stop
        self.score = score
        self.strand = strand
        self.frame = frame

    def __str__(self):
        attrs = []
        if self.ID:
            attrs.append('ID=' + self.ID)
        if self.Parent:
            attrs.append('Parent=' + self.Parent)
        return '\t'.join([self.reference_sequence, self.source, self.feature,
                          self.start, self.stop, self.score, self.strand,
                          self.frame, ';'.join(attrs)])

    __repr__ = __str__


class PredictedGene(list):

    def __init__(self, name):
        self.name = name
        self.coding_seq = ""
        self.protein_seq = ""

    def __str__(self):
        return "<Gene " + self.name + ", " + str(len(self)) + " predictions>"

    __repr__ = __str__


START_GENE = "# start gene "
CODING = '# coding sequence = ['
PROTEIN = '# protein sequence = ['


def parse_gff3(filename):
    predgenes = []
    curgene = None
    mode = ''

    for l in open(filename).xreadlines():
        l = l.strip()
        if l.startswith('#'):
            if mode == 'coding':
                if l.endswith(']'):
                    mode = ''
                    curgene.coding_seq += l[2:-1]
                else:
                    curgene.coding_seq += l[2:]
            elif mode == 'protein':
                if l.endswith(']'):
                    mode = ''
                    curgene.protein_seq += l[2:-1]
                else:
                    curgene.protein_seq += l[2:]
            elif mode == '':
                if l.startswith(START_GENE):
                    curgene = PredictedGene(l[len(START_GENE):])
                    predgenes.append(curgene)
                elif l.startswith(CODING):
                    mode = 'coding'
                    curgene.coding_seq = l[len(CODING):]
                elif l.startswith(PROTEIN):
                    mode = 'protein'
                    curgene.protein_seq = l[len(PROTEIN):]
        else:
            if curgene is None:
                curgene = PredictedGene("")
                predgenes.append(curgene)
            curgene.append(PredictedRegion(*l.split('\t')))
    return len(predgenes) == 1 and predgenes[0] or predgenes
