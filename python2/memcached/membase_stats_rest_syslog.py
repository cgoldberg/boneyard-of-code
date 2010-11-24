#!/usr/bin/env python
# Corey Goldberg - 2010
#
#  bucket statistics from Membase:
#  - prints formatted text report 
#  - writes tagged stats to unix syslog
#  - uses Membase Management REST API with HTTP Basic Authentication


import json
import urllib2
import syslog


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


output = []
output.append('bucket'.rjust(18))
for stat in sorted(results[0]['basicStats']):
    output.append(stat.rjust(18))
output.append('\n------------------------------------------------------------------------------------------------------------------------------\n')   
for bucket in sorted(results):
    name = bucket['name']
    stat_map = bucket['basicStats']
    output.append(name.rjust(18))
    for stat in sorted(stat_map):
        output.append(str(stat_map[stat]).rjust(18))
    output.append('\n')   
formatted_output = ''.join(output)

print formatted_output


output = []
for bucket in results:
    name = bucket['name']
    stat_map = bucket['basicStats']
    for stat in sorted(stat_map):
        output.append('%s-%s="%s"' % (name, stat, stat_map[stat]))  
tagged_output = ' '.join(output)

syslog.syslog(tagged_output)
    



#  Sample Console Output:
# 
# 
#              bucket       diskFetches          diskUsed         itemCount           memUsed         opsPerSec  quotaPercentUsed
#  ------------------------------------------------------------------------------------------------------------------------------
#             default                 0             10240                 0          25789640                 0     19.2147791386
#                 mb1                 0             10240                 0          25789640                 0     19.2147791386


#  Sample syslog entry:
#  
#  default-diskFetches="0" default-diskUsed="10240" default-itemCount="0" default-memUsed="25789640" default-opsPerSec="0"
#  default-quotaPercentUsed="19.2147791386" mb1-diskFetches="0" mb1-diskUsed="10240" mb1-itemCount="0" mb1-memUsed="25789640"
#  mb1-opsPerSec="0" mb1-quotaPercentUsed="19.21477913

