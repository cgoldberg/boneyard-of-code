#!/usr/bin/env python
# Corey Goldberg - 2010
# print a snapshot report of bucket statistics from Membase (Membase Management REST API)
# uses HTTP Basic Authentication



import json
import urllib2


NODE = '127.0.0.1'
PORT = '8091'
USERNAME = 'Administrator'
PASSWORD = 'PerfServer'


password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
uri = '%s:%s' % (NODE, PORT)
password_mgr.add_password(None, uri, USERNAME, PASSWORD)
auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(auth_handler)
urllib2.install_opener(opener)

url =  'http://%s:%s/pools/stats/buckets' % (NODE, PORT)

results = json.load(urllib2.urlopen(url))

print 'bucket'.rjust(18),
for stat in sorted(results[0]['basicStats']):
    print stat.rjust(18),
print '\n------------------------------------------------------------------------------------------------------------------------------'
for bucket in sorted(results):
    name = bucket['name']
    stat_map = bucket['basicStats']
    print name.rjust(18),
    for stat in sorted(stat_map):
        print str(stat_map[stat]).rjust(18),
       



#  Sample Output:
#
#
#             bucket       diskFetches          diskUsed         itemCount           memUsed         opsPerSec  quotaPercentUsed
# ------------------------------------------------------------------------------------------------------------------------------
#                mc1                 0                 0                 0                 0                 0               0.0
#                mc2                 0                 0                 0                 0                 0               0.0
#                mb1                 0            104448              3352          27191629                67    0.211034816069
#            default                 0            190464                10          25860014                 0     6.42240395149
           
           