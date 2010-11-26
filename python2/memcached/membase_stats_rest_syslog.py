#!/usr/bin/env python
# Corey Goldberg - 2010
#
#  bucket statistics from Membase:
#  - gets cluster 'basicStats' from Membase Management REST API (using HTTP Basic Authentication)
#  - produces tagged and/or formatted stats output
#  - writes to unix syslog
#  - prints to console/stdout



import json
import syslog
import urllib2



NODE = '127.0.0.1'
PORT = '8091'
USERNAME = 'Administrator'
PASSWORD = 'secret'

FORMATTED_DATA = True
TAGGED_DATA = True

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
    
    if FORMATTED_DATA:
        formatted_data = format(results)
        if SYSLOG_OUTPUT:
            syslog.syslog(formatted_data)
        if CONSOLE_OUTPUT:
            print formatted_data
            
    if TAGGED_DATA:
        tagged_data = tag(results)
        if SYSLOG_OUTPUT:
            syslog.syslog(tagged_data)
        if CONSOLE_OUTPUT:
            print tagged_data
            


def format(results):
    output = []
    output.append('bucket'.rjust(18))
    for stat in sorted(results[0]['basicStats']):
        output.append(stat.rjust(18))
    output.append('\n---------------------------------------------------------------' \
        '---------------------------------------------------------------\n')   
    for bucket in results:
        stat_map = bucket['basicStats']
        output.append(bucket['name'].rjust(18))
        for stat in sorted(stat_map):
            output.append(str(stat_map[stat]).rjust(18))
        output.append('\n')   
    formatted_output = ''.join(output)
    
    return formatted_output
    
    
    
def tag(results):
    output = []
    for bucket in results:
        stat_map = bucket['basicStats']
        for stat in sorted(stat_map):
            output.append('%s-%s="%s"' % (bucket['name'], stat, stat_map[stat]))  
    tagged_output = ' '.join(output)
    
    return tagged_output
    
    
    
    
if __name__== '__main__':
    main()




#  sample formatted output:
#
#              bucket       diskFetches          diskUsed         itemCount           memUsed         opsPerSec  quotaPercentUsed
#  ------------------------------------------------------------------------------------------------------------------------------
#             default                 0             10240                 0          25789640                 0     19.2147791386
#                 mb1                 0             10240                 0          25789640                 0     19.2147791386
#                 mc1                 0                 0                 0                 0                 0               0.0
#                 mc2                 0                 0                 0                 0                 0               0.0


#  sample tagged output:
#
#  default-diskFetches="0" default-diskUsed="10240" default-itemCount="0" default-memUsed="25789640" default-opsPerSec="0"
#  default-quotaPercentUsed="19.2147791386" mb1-diskFetches="0" mb1-diskUsed="10240" mb1-itemCount="0" mb1-memUsed="25789640"
#  mb1-opsPerSec="0" mb1-quotaPercentUsed="19.2147791386" mc1-diskUsed="0" mc1-hitRatio="0" mc1-itemCount="0" mc1-memUsed="0"
#  mc1-opsPerSec="0" mc1-quotaPercentUsed="0.0" mc2-diskUsed="0" mc2-hitRatio="0" mc2-itemCount="0" mc2-memUsed="0"
#  mc2-opsPerSec="0" mc2-quotaPercentUsed="0.0"