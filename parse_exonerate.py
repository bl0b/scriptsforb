from parse_gff2 import parse_gff2

START_GFF = "# --- START OF GFF DUMP ---"
END_GFF = "# --- END OF GFF DUMP ---"


class exonerate_file(file):

    def xreadlines(self):
        in_gff = False
        for l in file.xreadlines(self):
            if in_gff:
                yield l
            if l.startswith(START_GFF):
                in_gff = True
            elif l.startswith(END_GFF):
                in_gff = False


def parse_exonerate(filename):
    return parse_gff2(exonerate_file(filename))
