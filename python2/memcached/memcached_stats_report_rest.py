#!/usr/bin/env python
# Corey Goldberg - 2010
# print a 60 sec snapshot report of cache bucket statistics from Memcached (Membase Management REST API)

import json
import urllib


HOST = '127.0.0.1'
PORT = '8080'
BUCKET = 'my_bucket'


url =  'http://%s:%s/pools/default/buckets/%s/stats?stat=opsbysecond&period=1m' % (HOST, PORT, BUCKET)

results = json.load(urllib.urlopen(url))

print 'stat'.rjust(23), 'min'.rjust(12), 'avg'.rjust(12), 'max'.rjust(12)
print '-----------------------------------------------------------------'

for stat_name, values in sorted(results['op'].iteritems()):
    if stat_name not in ['samplesInterval', 'tstamp', 't']:
        mn = '%.0f' % min(values)
        mx = '%.0f' % max(values)
        avg = '%.2f' % (float(sum(values)) / len(values))
        print stat_name.rjust(23), mn.rjust(12), avg.rjust(12), mx.rjust(12)
    