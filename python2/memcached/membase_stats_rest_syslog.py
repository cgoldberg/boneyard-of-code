#!/usr/bin/env python
# Corey Goldberg - 2010
#
#  bucket statistics from Membase:
#  - writes tagged stats to unix syslog
#  - prints formatted text report 
#  - uses Membase Management REST API with HTTP Basic Authentication



import json
import syslog
import urllib2



NODE = '127.0.0.1'
PORT = '8091'
USERNAME = 'Administrator'
PASSWORD = 'secret'

SYSLOG_OUTPUT = True
CONSOLE_OUTPUT = True



def main():
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    uri = '%s:%s' % (NODE, PORT)
    password_mgr.add_password(None, uri, USERNAME, PASSWORD)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)

    url =  'http://%s:%s/pools/stats/buckets' % (NODE, PORT)

    results = json.load(urllib2.urlopen(url))

    if SYSLOG_OUTPUT:
        syslog.syslog(tag(results))
    if CONSOLE_OUTPUT:
        print format(results)



def tag(results):
    output = []
    for bucket in results:
        stat_map = bucket['basicStats']
        for stat in sorted(stat_map):
            output.append('%s-%s="%s"' % (bucket['name'], stat, stat_map[stat]))  
    tagged_output = ' '.join(output)
    
    return tagged_output



def format(results):
    output = []
    output.append('bucket'.rjust(18))
    for stat in sorted(results[0]['basicStats']):
        output.append(stat.rjust(18))
    output.append('\n---------------------------------------------------------------' \
        '---------------------------------------------------------------\n')   
    for bucket in sorted(results):
        stat_map = bucket['basicStats']
        output.append(bucket['name'].rjust(18))
        for stat in sorted(stat_map):
            output.append(str(stat_map[stat]).rjust(18))
        output.append('\n')   
    formatted_output = ''.join(output)
    
    return formatted_output
    
    
    
if __name__== '__main__':
    main()

    

#  sample console output:
# 
# 
#              bucket       diskFetches          diskUsed         itemCount           memUsed         opsPerSec  quotaPercentUsed
#  ------------------------------------------------------------------------------------------------------------------------------
#             default                 0             10240                 0          25789640                 0     19.2147791386
#                 mb1                 0             10240                 0          25789640                 0     19.2147791386


#  sample syslog entry:
#  
#  default-diskFetches="0" default-diskUsed="10240" default-itemCount="0" default-memUsed="25789640" default-opsPerSec="0"
#  default-quotaPercentUsed="19.2147791386" mb1-diskFetches="0" mb1-diskUsed="10240" mb1-itemCount="0" mb1-memUsed="25789640"
#  mb1-opsPerSec="0" mb1-quotaPercentUsed="19.21477913

