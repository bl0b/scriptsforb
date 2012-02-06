WIDTH = 71


class Sequence(object):

    def __init__(self, hdr, seq):
        self.header = hdr.strip()
        self.sequence = seq.strip()

    def __str__(self):
        ret = '>' + self.header + '\n'
        ret += '\n'.join(self.sequence[x:x + WIDTH]
                         for x in xrange(0, len(self.sequence), WIDTH))
        return ret


class Fasta(object):

    def __init__(self):
        self.seq_list = []
        self.seq_dic = {}

    def add_seq(self, seq):
        if seq.header in self.seq_dic:
            raise Exception("Duplicate fasta header " + seq.header)
        self.seq_dic[seq.header] = len(self.seq_list)
        self.seq_list.append(seq)

    def __len__(self):
        return len(self.seq_list)

    def __iter__(self):
        return iter(self.seq_list)

    def __getitem__(self, x):
        if type(x) is int:
            return self.seq_list[x]
        elif type(x) is str:
            return self.seq_list[self.seq_dic[x]]

    def read_from(self, filename):
        header = None
        sequence = None
        for line in open(filename).xreadlines():
            if line[0] == '>':
                if sequence is not None:
                    self.add_seq(Sequence(header, sequence))
                header = line[1:]
                sequence = ''
            else:
                sequence += line.strip()
        if sequence:
            self.add_seq(Sequence(header, sequence))

    def remove(self, x):
        if type(x) is int:
            s = self.seq_list[x]
            del self.seq_dic[s.header]
            del self.seq_list[x]
        elif type(x) is str:
            i = self.seq_dic[x]
            del self.seq_dic[x]
            del self.seq_list[i]

    def save_to(self, filename):
        f = open(filename, 'w')
        for s in self.seq_list:
            print >> f, s
