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
from datetime import datetime


ARGS = None
FIELDNAMES = ['Julian Time', 'Year-Month-Date Time', '6\"Sensor', '12\"Sensor'
              ,'18\"Sensor', 'Temp']


def main():
    usage = '%(prog)s <out_csv> <num_rows>'
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('out_csv', nargs=1,
                        help='output CSV file')
    parser.add_argument('num_rows', nargs=1,
                        help='# of rows to generate')
    global ARGS
    ARGS = parser.parse_args()
    # Open output csv
    try:
        with open(ARGS.out_csv[0], 'w') as csvfile:
            fieldnames = FIELDNAMES
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            dict = {}
            dict['Julian Time'] = time.time();
            for row in range(0, int(ARGS.num_rows[0])):
                oldtime = dict['Julian Time']
                newtime = random.randrange(int(oldtime), int(oldtime) + 900000)
                dict['Julian Time'] = newtime
                dict['Year-Month-Date Time'] = datetime.fromtimestamp(newtime).strftime('%Y-%m-%d %H:%M:%S')
                dict['6\"Sensor'] = random.randrange(0, 100)
                dict['12\"Sensor'] = random.randrange(0, 100)
                dict['18\"Sensor'] = random.randrange(0, 100)
                dict['Temp'] = random.randrange(20, 120)
                writer.writerow(dict)
    except IOError:
        print "Error: cannot open file:" + ARGS.out_csv[0]
        sys.exit(1)


if __name__ == '__main__':
    main()
