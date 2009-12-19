#!/usr/bin/env python
#  Copyright (c) 2009 Corey Goldberg (corey@goldb.org)
#
#  Multi-Process HTTP Load Generator


import httplib
import multiprocessing
import os
import Queue
import sys
import threading
import time
import urlparse



URL = 'http://www.example.com'
AGENTS = 2
INTERVAL = 1  # secs
RUN_TIME = 10  # secs
RAMPUP = 0  # secs



def main():
    manager = LoadManager()
    manager.start(AGENTS, INTERVAL, RUN_TIME, RAMPUP)
    


class LoadManager:
    def __init__(self):
        self.parsed_url = urlparse.urlsplit(URL)
        self.q = multiprocessing.Queue()       
        self.start_time = time.time()
        
    def start(self, agents=1, interval=0, run_time=10, rampup=0):
        rw = ResultWriter(self.q)
        rw.setDaemon(True)
        rw.start()
        
        for i in range(agents):
            spacing = (float(rampup) / float(agents))
            if i > 0:
                time.sleep(spacing)
            agent = LoadAgent(self.q, self.parsed_url, interval, self.start_time, run_time)
            print 'starting agent # %i' % i
            agent.start()



class LoadAgent(multiprocessing.Process):
    def __init__(self, queue, parsed_url, interval, start_time, run_time):
        multiprocessing.Process.__init__(self)
        self.q = queue
        self.interval = interval
        self.start_time = start_time
        self.run_time = run_time
        self.parsed_url = parsed_url
        
        # choose timer to use
        if sys.platform.startswith('win'):
            self.default_timer = time.clock
        else:
            self.default_timer = time.time
            
    def run(self):
        while True:
            start = self.default_timer()               
            try:
                self.send(self.parsed_url)
            except Exception, e:
                print e
            finish = self.default_timer()
            latency = finish - start
            elapsed = time.time() - self.start_time
            self.q.put((time.time(), latency))
            if elapsed >= self.run_time:
                break
            expire_time = self.interval - latency
            if expire_time > 0:
                time.sleep(expire_time)
           
    def send(self, parsed_url):
        if parsed_url.scheme.endswith('s'):
            conn = httplib.HTTPSConnection(parsed_url.netloc)
        else:
            conn = httplib.HTTPConnection(parsed_url.netloc)
        try:
            conn.request('GET', parsed_url.path, parsed_url.query)
            resp = conn.getresponse().read()
        except Exception, e:
            raise Exception('Connection Error: %s' % e)
        finally:
            conn.close()
    


class ResultWriter(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.q = queue
    
    def run(self):
        with open('results.csv', 'w') as f:     
            while True:
                try:
                    elapsed, latency = self.q.get(False)
                    f.write('%.3f,%.3f\n' % (elapsed, latency))
                    f.flush()
                    print '%.3f' % latency
                except Queue.Empty:
                    # re-check queue for messages every x sec
                    time.sleep(.1)



if __name__ == '__main__':
    main()
