

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



