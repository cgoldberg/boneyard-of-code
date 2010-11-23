#!/usr/bin/env python
# Corey Goldberg - 2010
# print a 60 sec snapshot report of bucket statistics from Membase (Membase Management REST API)
# uses HTTP Basic Authentication



import json
import urllib2


NODE = '192.168.12.171'
PORT = '8091'
USERNAME = 'Administrator'
PASSWORD = 'Secret'

DEBUG = False


password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
top_level = '%s:%s' % (NODE, PORT)
password_mgr.add_password(None, top_level, USERNAME, PASSWORD)
auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
if DEBUG:
    debug_handler = urllib2.HTTPHandler(debuglevel=1)
    opener = urllib2.build_opener(auth_handler, debug_handler)
else:
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