#!/usr/bin/env python
#  Copyright (c) 2008 Corey Goldberg (corey@goldb.org)
#
#  Single-threaded HTTP Load Generator


import sys
import time
import sys
import httplib


# URL parameters
USE_SSL = False  # HTTPS/SSL support
HOST = 'example.com'
PATH = '/'

INTERVAL = 0  # secs


def main():
    # choose timer to use
    if sys.platform.startswith('win'):
        default_timer = time.clock
    else:
        default_timer = time.time
    
    while True:
        msg = (HOST, PATH)
        start = default_timer()      
        try:
            send(msg)
        except:
            print 'request failed'
        finish = default_timer()
        latency = (finish - start)
        expire_time = (INTERVAL - latency)
        print '%.3f' % latency
        if expire_time > 0:
            time.sleep(expire_time)
                

def send(msg):
    if USE_SSL:
        conn = httplib.HTTPSConnection(msg[0])
    else:
        conn = httplib.HTTPConnection(msg[0])
    try:
        conn.request('GET', msg[1])
        conn.getresponse().read()
    finally:
        conn.close()       


if __name__ == '__main__':
    main()