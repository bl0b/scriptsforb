from parse_gff2 import parse_gff2
import re
from itertools import izip

START_GFF = "# --- START OF GFF DUMP ---"
END_GFF = "# --- END OF GFF DUMP ---"
C4_ALIGNMENT = 'C4 Alignment:'


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


c4 = ("         Query: gi|327271245|ref|XP_003220398.1| PREDICTED:"
      + " uncharacterized protein C6orf130-like isoform 1 [Anolis"
      + " carolinensis] >gi|327271247|ref|XP_003220399.1| PREDICTED:"
      + " uncharacterized protein C6orf130-like isoform 2 [Anolis"
      + """ carolinensis]
        Target: Gi_4536_gatcag5825_mbl1599_2MIRA_mapping Average"""
      + """ coverage: 73,89:[revcomp]
         Model: protein2dna:bestfit
     Raw score: 328
   Query range: 0 -> 150
  Target range: 1849 -> 1396

    1 : MetAlaSerIleAsnProGluLysGluGluArgIleValTyrArgGlnGlyAspLeuPheTh :   21
        :!::!!|||! !!.. !!   :!!:!!   ! !.!!..! ! ||||||||||||||||||||
        LeuSerSerThrThrSerIleGluLysPheThrPheThrGluArgGlnGlyAspLeuPheTh
 1849 : TTATCATCGACAACATCAATTGAAAAATTTACTTTTACAGAACGACAAGGAGACTTATTCAC : 1789

   22 : r<->CysProGluThrAspAlaLeuAlaHisCysIleSerGluAspCysHisMetSerAlaG :   41
        |   ...|||  !|||||||||||||||||||||:!!|||:!!|||  !...|||.!!  !|
        rAspAlaProProThrAspAlaLeuAlaHisCysValSerGlnAspLeuArgMetGlyLysG
 1788 : TGATGCACCACCAACTGACGCGTTAGCTCATTGCGTATCTCAAGATCTTAGAATGGGTAAAG : 1726

   42 : lyIleAlaAlaValPheLysLysLysPheGlyGlyIleGlnGluLeuLeuAsnGlnGlnLys :   61
        ||||||||  !:!!||||||||||||!:!! !|||:!!.!.||||||  !  !||||||""" + "   "
      + """
        lyIleAlaTyrIlePheLysLysLysTyrGluGlyLeuAsnGluLeuLysAlaGlnGlnCys
 1725 : GTATCGCATATATTTTCAAGAAAAAATATGAAGGATTAAATGAATTGAAAGCTCAACAATGT : 1666

   62 : LysThrGlyAspValAlaValLeuLysArgAspAsnArgTyrValTyrTyrLeuIleThrLy :   82
        |||..!|||.!.||||||  !|||:!!|||||||||||||||:!!!:!||||||||||||||
        LysValGlyGlnValAlaTyrLeuGlnArgAspAsnArgTyrIlePheTyrLeuIleThrLy
 1665 : AAAGTCGGTCAAGTTGCTTATCTTCAACGTGATAATCGTTATATTTTTTATTTAATTACTAA : 1603

   83 : sAsnLysTyrPheHisLysProThrTyrAspAsnLeuGlnLysSerLeuAspAlaMetLysL :  103
        | !! !   !!:! !!||||||  !  ! ! .!.!!!:!!! !||||||!  ! !:!!!:!""" + " "
      + """
        sTyrTyrValTyrAspLysProAspArgLysGluPheGluThrSerLeuValGluLeuArgA
 1602 : ATATTATGTTTACGATAAACCTGATCGTAAAGAATTTGAAACAAGTTTGGTGGAATTGAGAA : 1540

  104 : euHisCysValGluAsnGlyValThrArgIleSerMetProLysIleGlyCysGlyLeuAsp :  123
         !   |||! !:!!  !||||||! ! !!:!!|||:!:|||::!||||||  !|||||||||
        rgLeuCysGluGlnLeuGlyValArgGlyLeuSerValProArgIleGlyThrGlyLeuAsp
 1539 : GGTTGTGTGAACAACTTGGTGTTAGAGGTTTAAGTGTTCCTCGGATTGGAACTGGATTGGAT : 1480

  124 : ArgLeuAspTrpGluArgValSerThrMetLeuGluGluValPheGluGlyThrAspValTy :  144
         !!|||..!! !...  !|||!.!!:!   :!!.!.|||!.!|||||||||!:!:!!:!! !
        GlyLeuSerLeuSerTyrValLysSerAlaIleAsnGluAlaPheGluGlySerAsnIleLy
 1479 : GGGTTATCTTTGAGTTATGTTAAAAGTGCTATTAACGAAGCCTTTGAAGGGAGTAATATCAA : 1417

  145 : rIleThrValTyrIleLeu :  150
         :!!|||:!!!:!  !|||
        sValThrMetPheTyrLeu
 1416 : AGTTACTATGTTTTATTTG : 1397
""")


class Query(object):

    def __init__(self, f):

        def nextline():
            l = ''
            while not l:
                l = f.next()
            #print l
            return l

        self.raw_query = nextline().strip()
        q = self.raw_query[7:].split('PREDICTED: ')
        self.Query = q[0].strip()
        self.Predicted = len(q) > 1 and q[1].strip() or None
        self.raw_target = nextline().strip()
        t = self.raw_target[8:].split('Average coverage: ')
        self.Target = t[0].strip()
        self.AverageCoverage = len(t) > 1 and t[1].strip() or None
        self.raw_model = nextline().strip()
        self.Model = self.raw_model[7:]
        self.raw_raw_score = nextline().strip()
        self.RawScore = int(self.raw_raw_score[11:])
        self.raw_query_range = nextline().strip()
        self.QueryRange = self.raw_query_range.split(':')[1].split(' -> ')
        self.QueryRange = map(int, self.QueryRange)
        self.raw_target_range = nextline().strip()
        self.TargetRange = self.raw_target_range.split(':')[1].split(' -> ')
        self.TargetRange = map(int, self.TargetRange)

        self.query_prot = ""
        self.target_prot = ""
        self.target_seq = ""
        self.alignment = ""
        self.vulgar = ""
        self.gff = ""

        self.state = [self._rd_blank,
                      self._rd_q,
                      self._rd_al,
                      self._rd_tgt,
                      self._rd_dna]
        i = 0

        while self.state[i](nextline()):
            i = (i + 1) % len(self.state)
            #print i

    def iterate(self,
                pred_qp=lambda x: True,
                pred_tp=lambda x: True,
                pred_ts=lambda x: True,
                pred_a=lambda x: True):
        return ((qp, tp, ts, a)
                for qp, tp, ts, a in izip(self.query_prot, self.target_prot,
                                          self.target_seq, self.alignment)
                if pred_qp(qp) and pred_tp(tp)
                   and pred_ts(ts) and pred_a(a))

    def _rd_blank(self, l):
        return True

    def _rd_q(self, l):
        if l.startswith('vulgar'):
            return False
        #print "read query", l.strip()
        self.query_prot += l.split(' : ')[1]
        return True

    def _rd_al(self, l):
        #print "read alignment", l.strip()
        self.alignment += l[8:-1]
        return True

    def _rd_tgt(self, l):
        #print "read target", l.strip()
        self.target_prot += l[8:-1]
        return True

    def _rd_dna(self, l):
        #print "read target DNA", l.strip()
        s = l.split(' : ')
        self.target_seq += s[1]
        #print l
        #print "0123456789" * 8
        #print int(s[2].strip()), self.target_range[1]
        a = int(s[2].strip())
        b = self.TargetRange[1]
        return a != b and a != b + 1


class Exonerate(object):

    def __init__(self, filename):
        f = open(filename)
        self.commandline = re.match(r'Command line: \[([^]]*)',
                                    f.readline()).group(1)
        self.hostname = re.match(r'Hostname: \[([^]]*)',
                                 f.readline()).group(1)

        self.queries = []

        while True:
            try:
                l = f.next()
            except StopIteration, si:
                break
            if not l:
                continue
            if l.startswith(C4_ALIGNMENT):
                f.next()  # skip ------
                self.queries.append(Query(f))
            elif l.startswith('vulgar:'):
                self.queries[-1].vulgar = l[7:].strip()
            elif l.startswith(START_GFF):
                gff = []
                l = f.next()
                while not l.startswith(END_GFF):
                    gff.append(l)
                    l = f.next()
                self.queries[-1].gff = parse_gff2(iter(gff))
