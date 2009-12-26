#!/usr/bin/env python
#  Corey Goldberg, 2009 (corey@goldb.org)


import csv
from collections import defaultdict


def main():
    resp_times = parse_file('results.csv')
    chunked_series = split_series(resp_times, 1)
    with open('out.csv', 'w') as f:
        for i, seq in enumerate(chunked_series):
            f.write('%i,%i,%.3f\n' % (i, len(seq), avg(seq)))
    
    
def parse_file(file_name):
    reader = csv.reader(open(file_name, 'rb'))
    resp_times = [(float(line[0]), float(line[1])) for line in reader]
    return resp_times    
   
   
def split_series(points, interval):
    offset = points[0][0]
    maxval = int((points[-1][0] - offset) // interval)
    vals = defaultdict(list)
    for key, value in points:
        vals[(key - offset) // interval].append(value)
    series = [vals[i] for i in xrange(maxval + 1)]
    return series


def avg(seq):
    return float(sum(seq) / len(seq)) 
    


if __name__ == '__main__':
    main()
