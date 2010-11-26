#!/usr/bin/env python
# Corey Goldberg - 2010
#
#  bucket statistics from Membase:
#  - gets cluster 'basicStats' from Membase Management REST API (using HTTP Basic Authentication)
#  - produces formatted stats output report
#  - prints to console/stdout



import json
import urllib2



NODE = '127.0.0.1'
PORT = '8091'
USERNAME = 'Administrator'
PASSWORD = 'secret'



password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
uri = '%s:%s' % (NODE, PORT)
password_mgr.add_password(None, uri, USERNAME, PASSWORD)
auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(auth_handler)
urllib2.install_opener(opener)

url =  'http://%s:%s/pools/stats/buckets' % (NODE, PORT)

results = json.load(urllib2.urlopen(url))

print 'bucket'.rjust(18),
for stat_label in sorted(results[0]['basicStats']):
    print stat_label.rjust(18),
print '\n---------------------------------------------------------------' \
    '---------------------------------------------------------------'
for bucket in results:
    stat_map = bucket['basicStats']
    print bucket['name'].rjust(18),
    for stat in sorted(stat_map):
        print str(stat_map[stat]).rjust(18),
    print
print




#  sample output:
#  
#              bucket        diskFetches           diskUsed          itemCount            memUsed          opsPerSec   quotaPercentUsed 
#  ------------------------------------------------------------------------------------------------------------------------------
#             default                  0              10240                  0           25789640                  0      19.2147791386
#                 mb1                  0              10240                  0           25789640                  0      19.2147791386
#                 mc1                  0                  0                  0                  0                  0                0.0
#                 mc2                  0                  0                  0                  0                  0                0.0
#

           