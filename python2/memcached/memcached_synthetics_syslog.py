#!/usr/bin/env python
#  Corey Goldberg - 2010
#    - set/get a synthetic test key to measure latency
#    - run this script at regular intervals with a task/job scheduler
#    - writes to unix syslog
#    - requires python 2.x, python-memcached



import time
import memcache



# Config Settings
HOST = '192.168.12.171' 
PORT = '11211'
KEY_LENGTH = 30000  # bytes



def main():
    mc = memcache.Client(('%s:%s' % (HOST, PORT),))
    
    data = '*' * KEY_LENGTH  # 30kb value
    key = 'test_key_%s' % HOST
    
    try:
        set_latency_ms = set_key(mc, key, data)
    except MembaseException as e:
        set_latency_ms = str(e)
    
    try:
        get_latency_ms = get_key(mc, key)
    except MembaseException as e:
        get_latency_ms = str(e)
        
    output = '%s: setLatencyMS="%s",getLatencyMS="%s"' % (__file__, set_latency_ms, get_latency_ms)
    
    syslog.syslog(output)
    print output
    


def set_key(mc, key, data):
    start_timer = time.time()
    is_set = mc.set(key, data)
    stop_timer = time.time()
    set_latency_ms = (stop_timer - start_timer) * 1000
    if not is_set:
        raise MembaseException('Failed Set')
    return set_latency_ms


    
def get_key(mc, key):
    start_timer = time.time()
    value = mc.get(key)
    stop_timer = time.time()
    get_latency_ms = (stop_timer - start_timer) * 1000
    if value is None:
        raise MembaseException('Failed Get')
    return get_latency_ms
    

    
class MembaseException(Exception): pass



if __name__ == '__main__':
    main()



#
#  sample output:
#
#  memcached_synthetics_syslog.py: setLatencyMS="74.000120163",getLatencyMS="62.9999637604"
#
