#!/usr/bin/env python
#
#  Corey Goldberg - 2009, 2011 (goldb.org)
#
#  HTTP profiler - API performance probe
#   - sends synthetic transactions (HTTP requests) to an API
#   - stores response times in RRD database
#      - request sent
#      - response received
#      - content transferred
#   - generates PNG graphs from RRDs
#
#  Requirements:  Python 2.5+, RRDTool
#



import httplib
import os.path
import time
import urlparse
import rrd



HOST = 'http://192.168.1.5:8000'
URLS = (
    '%s/api/foo' % HOST,
    '%s/api/bar' % HOST,
    ) 
POLLING_INTERVAL = 30  # secs
GRAPH_MINS = (60, 720, 10080)


    
def main():
    parsed_urls = [urlparse.urlparse(url) for url in URLS]
    for parsed_url in parsed_urls:
        title = '%s.rrd' % parsed_url.path.replace('/', '_')
        if not os.path.exists(title):
            my_rrd = rrd.RRD(title)
            my_rrd.create_rrd(POLLING_INTERVAL)
    while True:
        start = time.time()
        for parsed_url in parsed_urls:
            title = '%s.rrd' % parsed_url.path.replace('/', '_')
            my_rrd = rrd.RRD(title)
            print '--------------------------------'
            print parsed_url.geturl()
            try:
                status, reason, size, request_time, response_time, transfer_time = timed_req(parsed_url)
                print '%s %s - %s' % (status, reason, time.strftime('%D %H:%M:%S', time.localtime()))
                print '%.0f ms => request sent' % request_time
                print '%.0f ms => response received' % response_time
                print '%.0f ms => content transferred (%i bytes)' % (transfer_time, size)
                times = (request_time, response_time, transfer_time)
                my_rrd.update(times)
                for mins in GRAPH_MINS:
                    my_rrd.graph(mins)
            except Exception as e:
                print 'failed: %s' % e
        elapsed = time.time() - start
        if POLLING_INTERVAL > elapsed:
            time.sleep(POLLING_INTERVAL - elapsed)
        


def timed_req(parsed_url):
    if parsed_url.scheme == 'https':
        conn = httplib.HTTPSConnection(parsed_url.netloc)
    else:
        conn = httplib.HTTPConnection(parsed_url.netloc)
    conn.set_debuglevel(0)
    start_timer = time.time()
    conn.request('GET', parsed_url.path)     
    request_timer = time.time()
    resp = conn.getresponse()
    response_timer = time.time()
    content = resp.read()
    conn.close()
    transfer_timer = time.time()
    size = len(content)
    
    assert resp.status == 200, resp.reason
    
    # convert to offset millisecs
    request_time = (request_timer - start_timer) * 1000
    response_time = (response_timer - start_timer) * 1000
    transfer_time = (transfer_timer - start_timer) * 1000
            
    return (
        resp.status,
        resp.reason,
        size,
        request_time, 
        response_time, 
        transfer_time, 
        )



if __name__ == '__main__':
    main()

