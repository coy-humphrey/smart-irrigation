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
    fieldnames = [x[0] for x in config.items('Fieldnames')]
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
            dict = {}
            newtime = time.time()
            for row in range(0, int(ARGS.num_rows[0])):
                oldtime = newtime
                newtime = random.randrange(int(oldtime), int(oldtime) + 900000)
                dict['time'] = datetime.fromtimestamp(newtime).strftime('%Y-%m-%d %H:%M:%S')
                dict['s1'] = random.randrange(0, 100)
                dict['s2'] = random.randrange(0, 100)
                dict['s3'] = random.randrange(0, 100)
                dict['temp'] = random.randrange(20, 120)
                writer.writerow(dict)
    except IOError:
        print "Error: cannot open file:" + ARGS.out_csv[0]
        sys.exit(1)


if __name__ == '__main__':
    main()
