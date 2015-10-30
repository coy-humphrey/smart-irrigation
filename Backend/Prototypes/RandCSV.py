#!/usr/bin/python

"""Script for generating random values for smart-irrigation
csv templates

Contains methods for:
    -- generating csv files with random row values.
"""

__author__ = 'Ryan Fulscher <rfulsche@ucsc.edu>'

import argparse
import sys
import csv
import random
import time
import ConfigParser
from datetime import datetime


ARGS = None


def main():
    usage = '%(prog)s <out_csv> <num_rows>'
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
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('out_csv', nargs=1,
                        help='output CSV file')
    parser.add_argument('num_rows', nargs=1,
                        help='# of rows to generate')
    global ARGS
    ARGS = parser.parse_args()
    # Open output csv
    try:
        with open(ARGS.out_csv[0], 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            newtime = time.time()
            for rownum in range(0, int(ARGS.num_rows[0])):
                row = {}
                for datepair in config.items('Dates'):
                    oldtime = newtime
                    newtime = int(oldtime) + 900
                    timeformat = config.get('Dates', datepair[0])
                    row[datepair[0]] = datetime.fromtimestamp(newtime).strftime(timeformat)
                for pair in config.items('Integers'):
                    randmin = int(config.get('Integers', pair[0]).split(',')[0])
                    randmax = int(config.get('Integers', pair[0]).split(',')[1])
                    row[pair[0]] = random.randrange(randmin, randmax)
                writer.writerow(row)
    except IOError:
        print "Error: cannot open file:" + ARGS.out_csv[0]
        sys.exit(1)


if __name__ == '__main__':
    main()
