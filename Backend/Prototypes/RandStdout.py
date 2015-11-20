#!/usr/bin/python

"""Script for generating random values for smart-irrigation

"""

__author__ = 'Ryan Fulscher <rfulsche@ucsc.edu>'

import argparse
import sys
import csv
import random
import time
import ConfigParser
import threading
from datetime import datetime


ARGS = None

def main():
    threading.Timer(900.0, main).start()
    aggregate()

def aggregate():
    usage = '%(prog)s'
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    try:
        config.read('RandCSV.cfg')
    except IOError:
        print "Error: cannot open config file: RandCSV.cfg"
        sys.exit(1)
    fieldnames = []
    for section in config.sections():
        for setting in [x[0] for x in config.items(section)]:
            fieldnames.append(setting)
    global ARGS
#prints a list to stdout that holds values for time, s1, s2, s3, and temp in respective order
    try:
        row = []
        for datepair in config.items('Dates'):
            timeformat = config.get('Dates', datepair[0])
            row.append((datepair[0], datetime.now().strftime(timeformat)))
        for pair in config.items('Integers'):
            randmin = int(config.get('Integers', pair[0]).split(',')[0])
            randmax = int(config.get('Integers', pair[0]).split(',')[1])
            row.append((pair[0], random.randrange(randmin, randmax)))
        print(row)
    except IOError:
        print "Error: cannot print to stdout"
        sys.exit(1)


if __name__ == '__main__':
    main()
