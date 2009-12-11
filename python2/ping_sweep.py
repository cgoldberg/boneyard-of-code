#!/usr/bin/env python
# Corey Goldberg - 2008


import sys
import re
from subprocess import Popen, PIPE
from threading import Thread


num_threads = 128


def main():
    if len(sys.argv) != 1:
        ip_stem = sys.argv[1]
        if not re.match('^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$', ip_stem):
            print 'error: invalid ip_stem'
            print 'example: ping_sweep.py 192.168.1'
            sys.exit(1)
    else:
        print 'usage: ping_sweep.py ip_stem'
        print 'example: ping_sweep.py 192.168.1'
        sys.exit(1)
    ips = ['%s.%i' % (ip_stem, ip_end) for ip_end in xrange(256)]
    ip_buckets = split_seq(ips, num_threads)
    ip_buckets = []
    for seq in split_seq(ips, num_threads):
        ip_buckets.append(seq)
    PingSweep(ip_buckets)
    
def split_seq(seq, num_pieces):
    start = 0
    for i in xrange(num_pieces):
        stop = start + len(seq[i::num_pieces])
        yield seq[start:stop]
        start = stop

        
class PingSweep(object):
    def __init__(self, ip_buckets):
        print 'pinging hosts:\n'
        for thread_ref, ip_bucket in zip(range(num_threads), ip_buckets):
            sa = SweepAgent(ip_bucket)
            sa.start()
        
        
class SweepAgent(Thread):
    def __init__(self, ip_bucket):
        Thread.__init__(self)        
        self.ip_bucket = ip_bucket

    def run(self):
        for ip in self.ip_bucket:
            p = Popen('ping -n 1 ' + ip, stdout=PIPE)
            m = re.search('Average = (.*)ms', p.stdout.read())
            if m:
                print '%s is alive.  round trip time: %s ms' % (ip, m.group(1))
              
                             
if __name__ == '__main__':
    main()
        
