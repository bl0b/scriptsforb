#!/usr/bin/python

import re
import sys
import urllib
import urllib2


# query http://frodo.wi.mit.edu/primer3/ from command-line

print ("This script queries http://frodo.wi.mit.edu/primer3/. " +
       "Use with all due respect.")

new_state = {}
behaviour = {'fast': False, 'output': sys.stdout}

host = "http://frodo.wi.mit.edu"
init_url = host + "/primer3/"

# as of 6 may 2011
post_url = ("http://frodo.wi.mit.edu/cgi-bin/primer3-web-cgi-bin-0.4.0/" +
            "primer3_results.cgi")
state = {
    'PRIMER_INSIDE_PENALTY': '',
    'PRIMER_FIRST_BASE_INDEX': '1',
    'PRIMER_INTERNAL_OLIGO_OPT_TM': '60.0',
    'PRIMER_PAIR_WT_PRODUCT_SIZE_LT': '0.0',
    'PRIMER_IO_WT_SIZE_LT': '1.0',
    'PRIMER_WT_TM_LT': '1.0',
    'PRIMER_INTERNAL_OLIGO_MIN_SIZE': '18',
    'INCLUDED_REGION': '',
    'PRIMER_SALT_CONC': '50.0',
    'MUST_XLATE_PICK_RIGHT': '1',
    'PRIMER_PRODUCT_SIZE_RANGE': '150-250 100-300 301-400 401-500 501-600' +
                                 '601-700 701-850 851-1000',
    'PRIMER_INTERNAL_OLIGO_MAX_POLY_X': '5',
    'PRIMER_MAX_POLY_X': '5',
    'PRIMER_INTERNAL_OLIGO_NUM_NS': '0',
    'PRIMER_WT_NUM_NS': '0.0',
    'PRIMER_SALT_CORRECTIONS': '',
    'PRIMER_WT_GC_PERCENT_LT': '0.0',
    'PRIMER_INTERNAL_OLIGO_MAX_GC': '80.0',
    'PRIMER_IO_WT_COMPL_ANY': '0.0',
    'PRIMER_WT_REP_SIM': '0.0',
    'PRIMER_WT_GC_PERCENT_GT': '0.0',
    'PRIMER_LIBERAL_BASE': '1',
    'PRIMER_MIN_QUALITY': '0',
    'PRIMER_WT_TEMPLATE_MISPRIMING': '0.0',
    'PRIMER_WT_COMPL_ANY': '0.0',
    'PRIMER_OPT_SIZE': '20',
    'PRIMER_MAX_MISPRIMING': '12.00',
    'PRIMER_PAIR_WT_IO_PENALTY': '0.0',
    'PRIMER_IO_WT_TM_LT': '1.0',
    'PRIMER_QUALITY_RANGE_MIN': '0',
    'PRIMER_INTERNAL_OLIGO_MAX_SIZE': '27',
    'PRIMER_WT_SEQ_QUAL': '0.0',
    'PRIMER_WT_TM_GT': '1.0',
    'PRIMER_PAIR_WT_COMPL_ANY': '0.0',
    'PRIMER_NUM_RETURN': '5',
    'PRIMER_PRODUCT_MAX_TM': '',
    'PRIMER_MIN_END_QUALITY': '0',
    'PRIMER_DNTP_CONC': '0.0',
    'PRIMER_PRODUCT_MIN_TM': '',
    'PRIMER_WT_COMPL_END': '0.0',
    'PRIMER_PAIR_WT_REP_SIM': '0.0',
    'PRIMER_DNA_CONC': '50.0',
    'PRIMER_INTERNAL_OLIGO_MISHYB_LIBRARY': '',
    'PRIMER_IO_WT_SEQ_QUAL': '0.0',
    'PRIMER_INTERNAL_OLIGO_DIVALENT_CONC': '0.0',
    'PRIMER_OPT_TM': '60.0',
    'PRIMER_INTERNAL_OLIGO_SALT_CONC': '50.0',
    'PRIMER_PAIR_WT_COMPL_END': '0.0',
    'PRIMER_MIN_SIZE': '18',
    'PRIMER_QUALITY_RANGE_MAX': '100',
    'PRIMER_SELF_END': '3.00',
    'MUST_XLATE_PICK_LEFT': '1',
    'PRIMER_MAX_TEMPLATE_MISPRIMING': '12.00',
    'PRIMER_IO_WT_NUM_NS': '0.0',
    'PRIMER_PAIR_WT_PRODUCT_TM_LT': '0.0',
    'PRIMER_WT_END_STABILITY': '0.0',
    'PRIMER_MIN_GC': '20.0',
    'PRIMER_INTERNAL_OLIGO_MAX_TM': '63.0',
    'PRIMER_OPT_GC_PERCENT': '',
    'PRIMER_NUM_NS_ACCEPTED': '0',
    'PRIMER_WT_SIZE_GT': '1.0',
    'PRIMER_INTERNAL_OLIGO_MIN_QUALITY': '0',
    'PRIMER_PAIR_WT_DIFF_TM': '0.0',
    'PRIMER_INTERNAL_OLIGO_DNA_CONC': '50.0',
    'PRIMER_PAIR_WT_PRODUCT_SIZE_GT': '0.0',
    'PRIMER_IO_WT_SIZE_GT': '1.0',
    'PRIMER_PAIR_WT_PRODUCT_TM_GT': '0.0',
    'Pick Primers': 'Pick Primers',
    'PRIMER_MAX_GC': '80.0',
    'PRIMER_INTERNAL_OLIGO_MIN_GC': '20.0',
    'PRIMER_PAIR_WT_TEMPLATE_MISPRIMING': '0.0',
    'PRIMER_IO_WT_GC_PERCENT_LT': '0.0',
    'PRIMER_INTERNAL_OLIGO_EXCLUDED_REGION': '',
    'PRIMER_MIN_TM': '57.0',
    'SEQUENCE': '',
    'PRIMER_PAIR_WT_PR_PENALTY': '1.0',
    'TARGET': '',
    'PRIMER_INTERNAL_OLIGO_MAX_MISHYB': '12.00',
    'PRIMER_PAIR_MAX_MISPRIMING': '24.00',
    'PRIMER_WT_END_QUAL': '0.0',
    'PRIMER_GC_CLAMP': '0',
    'PRIMER_DIVALENT_CONC': '0.0',
    'PRIMER_MAX_END_STABILITY': '9.0',
    'PRIMER_SEQUENCE_ID': '',
    'PRIMER_START_CODON_POSITION': '',
    'PRIMER_INTERNAL_OLIGO_MIN_TM': '57.0',
    'PRIMER_IO_WT_TM_GT': '1.0',
    'PRIMER_LOWERCASE_MASKING': '1',
    'PRIMER_INTERNAL_OLIGO_DNTP_CONC': '0.0',
    'PRIMER_SELF_ANY': '8.00',
    'PRIMER_IO_WT_GC_PERCENT_GT': '0.0',
    'PRIMER_INTERNAL_OLIGO_SELF_END': '12.00',
    'PRIMER_MISPRIMING_LIBRARY': '',
    'PRIMER_MAX_SIZE': '27',
    'EXCLUDED_REGION': '',
    'MUST_XLATE_PRINT_INPUT': '1',
    'PRIMER_RIGHT_INPUT': '',
    'PRIMER_INTERNAL_OLIGO_OPT_SIZE': '20',
    'PRIMER_IO_WT_REP_SIM': '0.0',
    'PRIMER_INTERNAL_OLIGO_OPT_GC_PERCENT': '',
    'PRIMER_LIB_AMBIGUITY_CODES_CONSENSUS': '0',
    'PRIMER_OUTSIDE_PENALTY': '0',
    'PRIMER_MAX_TM': '63.0',
    'PRIMER_TM_SANTALUCIA': '',
    'PRIMER_WT_SIZE_LT': '1.0',
    'PRIMER_PRODUCT_OPT_TM': '',
    'PRIMER_WT_POS_PENALTY': '0.0',
    'PRIMER_MAX_DIFF_TM': '100.0',
    'PRIMER_INTERNAL_OLIGO_SELF_ANY': '12.00',
    'PRIMER_LEFT_INPUT': '',
    'PRIMER_INTERNAL_OLIGO_INPUT': '',
    'PRIMER_PAIR_MAX_TEMPLATE_MISPRIMING': '24.00'
}


def init_query():
    global state, post_url
    stream = urllib.urlopen(init_url)
    buf = ""
    while True:
        data = stream.read(1024)
        if not data:
            break
        buf += data
    m = (re.findall('select name="([^"]*)"()', buf) +
         re.findall('name="([^"]*)" value="([^"]*)"', buf) +
         re.findall('textarea name="([^"]*)"()', buf))
    print m
    state = dict(m)
    post_url = (host +
                re.compile('form action="([^"]*)"').search(buf).groups()[0])
    print state


def post_data():
    data = urllib.urlencode(state.items())
    req = urllib2.Request(post_url)
    print req, data
    fd = urllib2.urlopen(req, data)
    buf = ""
    while True:
        data = fd.read(1024)
        if not data:
            break
        buf += data
    return buf


def init_args(args):
    global new_state, behaviour
    for i in xrange(1, len(args)):
        if args[i] in ['-f', '--fast']:
            behaviour["fast"] = True
        elif args[i] in ['-o', '--output']:
            i += 1
            behaviour["output"] = open(args[i], 'w')
        elif args[i] in ['-h', '--help']:
            print "Query Primer3"
            print "by Damien Leroux <damien.leroux@gmail.com>"
            print
            print "Usage: %s [-f,--fast] [-o,--output filename]",
            print "[configuration_key=value...]" % args[0]
            print "Configuration keys:"
            for (k, v) in filter(lambda x: ' ' not in x, state.items()):
                if v:
                    print ' ', k.lower(), '(default %s)' % v
                else:
                    print ' ', k.lower()
            sys.exit(0)
        else:
            key, value = args[i].split("=")
            key = key.upper()
            if ' ' not in key and key in state:
                new_state[key] = value
            else:
                print "I don't know nothing about a '%s', I do mean it." % key
                sys.exit(1)


def update_state():
    state.update(new_state)


if __name__ == '__main__':
    init_args(sys.argv)
    if not behaviour["fast"]:
        init_query()
    #print state
    update_state()
    #print post_url
    buf = post_data()
    print >> behaviour['output'], buf
