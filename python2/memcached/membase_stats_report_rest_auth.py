#!/usr/bin/env python
# Corey Goldberg - 2010
# print a 60 sec snapshot report of pool statistics from Membase (Membase Management REST API)
# uses HTTP Basic Authentication



import json
import urllib2



NODE = '192.168.12.171'
PORT = '8091'
USERNAME = 'Administrator'
PASSWORD = 'Secret'



url =  'http://%s:%s/pools/default/stats?stat=opsbysecond&period=1m' % (NODE, PORT)
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
top_level = '%s:%s' % (NODE, PORT)
password_mgr.add_password(None, top_level, USERNAME, PASSWORD)
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

response = urllib2.urlopen(url)
results = json.load(response)


print 'stat'.rjust(23), 'min'.rjust(15), 'avg'.rjust(15), 'max'.rjust(15)
print '-----------------------------------------------------------------------'
   
for stat_name, values in sorted(results['op']['samples'].iteritems()):
    if stat_name not in ['timestamp']:
        mn = '%.0f' % min(values)
        mx = '%.0f' % max(values)
        avg = '%.2f' % (float(sum(values)) / len(values))
        print stat_name.rjust(23), mn.rjust(15), avg.rjust(15), mx.rjust(15)
        


