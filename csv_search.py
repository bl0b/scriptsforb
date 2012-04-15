#!/usr/bin/env python

from itertools import ifilter
from csv_parser import Csv
import sys
import re
from jupyLR import Scanner, Automaton
from optparse import OptionParser


#

SE_grammar = """
-colname
    = STRING
    | WHATEVER

colset
    = _colset

-_colset
    = _colset COMMA colname
    | colname

-value
    = STRING
    | WHATEVER

valueset
    = _valueset

-_valueset
    = _valueset COMMA value
    | value

-where
    = p4

p1  = colset EQ valueset
    | colset MATCHES valueset
    | colset CONTAINS valueset

-p1 = OPEN_PAR where CLOSE_PAR

-p2 = p1
p2  = NOT p2

-p3 = p2
p3  = p2 AND p3

-p4 = p3
p4  = p3 OR p4
"""


class Predicate(object):
    pass


class ColumnPredicate(Predicate):

    def __init__(self, cols, values):
        self.cols = cols
        self.values = values

    def __call__(self, row):
        return reduce(bool.__or__,
                      (reduce(lambda a, v: a or self.eval(c, v),
                             self.values, False)
                      for c in (row[i].lower() for i in self.cols)))


class Eq(ColumnPredicate):

    def __init__(self, col, value):
        ColumnPredicate.__init__(self, col, value)
        self.values = [v.lower() for v in self.values]

    def eval(self, c, v):
        return c == v


class Contains(ColumnPredicate):

    def __init__(self, col, value):
        ColumnPredicate.__init__(self, col, value)
        self.values = [v.lower() for v in self.values]

    def eval(self, c, v):
        return v in c


class Matches(ColumnPredicate):

    def __init__(self, col, value):
        ColumnPredicate.__init__(self, col, value)
        self.value = re.compile(self.value, re.IGNORECASE)

    def eval(self, c, v):
        return v.match(c) is not None


class BinaryPredicate(Predicate):

    def __init__(self, a, b):
        self.a = a
        self.b = b


class And(BinaryPredicate):

    def __call__(self, row):
        return self.a(row) and self.b(row)


class Or(BinaryPredicate):

    def __call__(self, row):
        return self.a(row) or self.b(row)


class Not(Predicate):

    def __init__(self, a):
        self.a = a

    def __call__(self, row):
        return not self.a(row)


class SE_Parser(Automaton):

    def __init__(self, csv):
        SE_scanner = Scanner(STRING=r'"((?:\\["\tvbnr]|[^\"])*)"',
                             AND=r"\band\b",
                             OR=r"\bor\b",
                             NOT=r"\bnot\b",
                             EQ="=",
                             COMMA=",",
                             MATCHES=r"\bmatches\b",
                             CONTAINS=r"\bcontains\b",
                             OPEN_PAR="[(]",
                             CLOSE_PAR="[)]",
                             _whitespace=r"[ \r\n\t]+",
                            discard_names=["_whitespace"])
        SE_scanner.add(WHATEVER=r"[^ ,\r\n\t=()]+")
        Automaton.__init__(self, "where", SE_grammar, SE_scanner)
        if csv.headers:
            self.colnames = dict((k, v)
                                 for v in xrange(len(csv.headers))
                                 for k in (v + 1, str(v + 1), csv.headers[v]))
        else:
            self.colnames = dict((k, i)
                                 for i in xrange(len(csv.data[0]))
                                 for k in (str(i + 1), i + 1))
        self.val = {
            'p1': self.p1,
            'p2': self.p2,
            'p3': self.p3,
            'p4': self.p4,
            'colset': self.colset,
            'valueset': self.valueset,
        }

    def colset(self, ast):
        return tuple(self.colnames[a[1]] for a in ast[1::2])

    def valueset(self, ast):
        return tuple(a[1] for a in ast[1::2])

    def p1(self, ast):
        op = {'EQ': Eq,
              'MATCHES': Matches,
              'CONTAINS': Contains
             }[ast[2][0]]
        return op(ast[1], ast[3])

    def p2(self, ast):
        return Not(ast[2])

    def p3(self, ast):
        return And(ast[1], ast[3])

    def p4(self, ast):
        return Or(ast[1], ast[3])

    def validate_ast(self, ast):
        return self.val[ast[0]](ast)


def search_csv(csv, query):
    se = SE_Parser(csv)
    pred = se(query)[0]
    return ifilter(pred, csv.data)


if __name__ == '__main__':
    op = OptionParser()
    op.add_option("-s", "--separator", dest="sep",
                  help="CSV separator (default: tab)", default="\t")
    op.add_option("-n", "--no-header", dest="nh", action="store_true",
                  default=False, help="Don't use first row as column names")

    op.usage += ' [<CSV file> "query"]...'

    op.usage += """

Where query is a predicate on one or more columns in the CSV.
A column name is either its number (starting from 1) and/or the value in this
column in the first row if the -n option was not specified.
A value is anything. Use double quotes to enclose values containing spaces.

Column predicates are case-insensitive.

Column predicates are :
    COLNAME contains VALUE          the string VALUE appears anywhere inside
                                    the column value.
    COLNAME = VALUE                 the column value is exactly VALUE.
    COLNAME matches VALUE           VALUE is a regular expression and the
                                    value in the column matches it.

Combinations are (A and B are any column predicate or any predicate already
mentioned):
    ( predicate )                   sub-expression grouping
    not A                           true if A evaluates to false
    A and B                         true if A and B both evaluate to true
    A or B                          true if any of A or B evaluate to true
"""

    opts, args = op.parse_args(sys.argv[1:])

    for i in xrange(0, len(args), 2):
        csv = Csv(args[i], sep=opts.sep, headers=not opts.nh)
        if csv.headers:
            print opts.sep.join(csv.headers)
        for row in search_csv(csv, args[i + 1]):
            print "\t".join('"' + str(v) + '"' for v in row)
