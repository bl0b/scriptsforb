#!/usr/bin/env python

from itertools import ifilter
from csv_parser import Csv
import sys
import re
from jupyLR import Scanner, Automaton


#

SE_grammar = """
-colname
    = STRING
    | WHATEVER

-value
    = STRING
    | WHATEVER

-where
    = p4

p1  = colname EQ value
    | colname MATCHES value
    | colname CONTAINS value

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

    def __init__(self, col, value):
        self.col = col
        self.value = value

    def __call__(self, row):
        return self.eval(row[self.col])


class Eq(ColumnPredicate):

    def eval(self, v):
        return v == self.value


class Contains(ColumnPredicate):

    def eval(self, v):
        return self.value in v


class Matches(ColumnPredicate):

    def __init__(self, col, value):
        ColumnPredicate.__init__(self, col, value)
        self.value = re.compile(self.value)

    def eval(self, v):
        return self.value.match(v) is not None


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
                             MATCHES=r"\bmatches\b",
                             CONTAINS=r"\bcontains\b",
                             _whitespace=r"[ \r\n\t]+",
                            discard_names=["_whitespace"])
        SE_scanner.add(WHATEVER=r"[^ \r\n\t=]+")
        Automaton.__init__(self, "where", SE_grammar, SE_scanner)
        self.colnames = dict((k, v)
                             for v in xrange(len(csv.headers))
                             for k in (v, str(v), csv.headers[v]))
        self.val = {
            'p1': self.p1,
            'p2': self.p2,
            'p3': self.p3,
            'p4': self.p4
        }

    def p1(self, ast):
        op = {'EQ': Eq,
              'MATCHES': Matches,
              'CONTAINS': Contains
             }[ast[2][0]]
        return op(self.colnames[ast[1][1]], ast[3][1])

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
    for i in xrange(1, len(sys.argv), 2):
        csv = Csv(sys.argv[i])
        for row in search_csv(csv, sys.argv[i + 1]):
            print "\t".join('"' + str(v) + '"' for v in row)
