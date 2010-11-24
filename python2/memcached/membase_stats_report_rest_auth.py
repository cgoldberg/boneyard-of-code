#!/usr/bin/env python
# Corey Goldberg - 2010
# print a snapshot report of bucket statistics from Membase (Membase Management REST API)
# uses HTTP Basic Authentication



import json
import urllib2


NODE = '127.0.0.1'
PORT = '8091'
USERNAME = 'Administrator'
PASSWORD = 'Secret'


password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
uri = '%s:%s' % (NODE, PORT)
password_mgr.add_password(None, uri, USERNAME, PASSWORD)
auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(auth_handler)
urllib2.install_opener(opener)


url =  'http://%s:%s/pools/stats/buckets' % (NODE, PORT)

results = json.load(urllib2.urlopen(url))

print 'bucket'.rjust(15), 'item count'.rjust(15), 'mem used'.rjust(18)
print '--------------------------------------------------'

for bucket in sorted(results):
    name = bucket['name']
    stat_map = bucket['basicStats']
    count = str(stat_map['itemCount'])
    mem_used = str(stat_map['memUsed'])
    print name.rjust(15), count.rjust(15), mem_used.rjust(18)




# Sample Output:
# 
# 
#          bucket      item count           mem used
# --------------------------------------------------
#             mc1               0                  0
#             mc2               0                  0
#             mb1               0           25790864
#         default              10           25858790
# 