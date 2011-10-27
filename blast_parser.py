

# Assume that line is :
# Fields: Query id, Subject id, % identity, alignment length, mismatches, gap openings, q. start, q. end, s. start, s. end, e-value, bit score
BlastFields = ('Query id', 'Subject id', '% identity', 'alignment length', 'mismatches', 'gap openings', 'q. start', 'q. end', 's. start', 's. end', 'e-value', 'bit score')

def split_blast_line(line):
    bf = filter(lambda x : len(x)>0, line.strip().split('\t'))
    if len(bf)!=len(BlastFields):
        raise Exception("error at line \""+line+"\"")
    return bf


def parse_blast_line(line):
    if line.startswith("#"):
        return None
    return dict(zip(BlastFields, split_blast_line(line)))

def extract_blast_fields(line, *fields):
    bf = split_blast_line(line)
    ret = []
    for f in fields:
        ret.append(bf[f])
    return ret


def read_blast(blast, filt, pp):
    f = open(blast)
    for l in f.xreadlines():
        if not l.startswith('#') and filt(l):
            pp(l)



# BLASTN 2.2.20 [Feb-08-2009]# Query: F2D1W4Z01DHZ76 
# Database: genbank_phage 172 
# Fields: Query id, Subject id, % identity, alignment length, mismatches, gap openings, q. start, q. end, s. start, s. end, e-value, bit score

class result(object):
    def __init__(self):
        #dict.__init__(self)
        self.data = []
        self.version = None
        self.query = None
        self.fields = None
        self.database = None
    def headers(self, field_list=None):
        return '# '+self.version+'# Query: '+self.query+'\n# Database: '+self.database+'\n# Fields: '+', '.join(field_list or self.fields)
    def __str__(self):
        return self.headers()+'\n'+'\n'.join(('\t'.join(r) for r in self.data))
    def __repr__(self):
        return "<BLAST result (%s @ %s), %i rows>"%(self.query, self.database, len(self.data))
    class row(list):
        def __init__(self, fields, data):
            list.__init__(self, data)
            self.fields = dict((k, i) for i, k in enumerate(fields))
            self.fields.update(dict((i, i) for i in xrange(len(fields))))
        def __call__(self, k):
            return self[self.fields[k]]
        def format(self, fmt):
            parts = [ x.split('}') for x in fmt.split('{') ]
            ret = []
            for p in parts:
                if len(p)==2:
                    ret.append(self(p[0]))
                ret.append(p[-1])
            return ''.join(ret)
    def add_row(self, data):
        self.data.append(result.row(self.fields, data))
    def format(self, headers=False, fmt=None):
        ret = headers and [self.headers(type(fmt) is list and fmt or None)] or []
        if fmt is None:
            fmt_row = lambda r: '\t'.join(r)
        elif type(fmt) is list:
            fmt_row = lambda r: '\t'.join((r(x) for x in fmt))
        elif type(fmt) is str:
            fmt_row = lambda r: r.format(fmt)
        for r in self.data:
            ret.append(fmt_row(r))
        return '\n'.join(ret)

def parse_file(f):
    results = []
    edit = None
    for l in (type(f) is str and open(f) or f).xreadlines():
        if l.startswith('#'):
            for piece in (p.strip() for p in l.split('#') if len(p)>0):
                if piece.startswith('BLA'): # could be BLAT, BLASTN...
                    if edit is not None:
                        results.append(edit)
                    edit = result()
                    edit.version = piece
                elif piece.startswith('Query'):
                    edit.query = piece[7:]
                elif piece.startswith('Database'):
                    edit.database = piece[10:]
                elif piece.startswith('Fields'):
                    edit.fields = [fld.strip() for fld in piece[8:].split(',')]
        else:
            edit.add_row([field.strip() for field in l.strip().split('\t')])
            #edit.data.append([field.strip() for field in l.strip().split('\t')])
    if edit is not None:
        results.append(edit)
    return results

