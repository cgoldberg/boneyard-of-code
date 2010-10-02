#!/usr/bin/env python
#  Copyright (c) 2008-2009 Corey Goldberg (corey@goldb.org)
#
#  Multithreaded HTTP Load Generator


import time
import sys
import os
import httplib
from threading import Thread, Lock



# URL parameters
USE_SSL = False  # HTTPS/SSL support
HOST = 'example.com'
PATH = '/'

# load parameters
THREADS = 1
INTERVAL = 0  # secs
RAMPUP = 0  # secs



def main():
    manager = LoadManager()
    manager.msg = (HOST, PATH)
    manager.start(THREADS, INTERVAL, RAMPUP)
    
    
    
class LoadManager:
    def __init__(self):
        self.msg = ('localhost', '/')
        self.start_time = time.time()      
        

    def start(self, threads=1, interval=0, rampup=0):
        try:
            os.remove('results.csv')
        except:
            pass
        for i in range(threads):
            spacing = (float(rampup) / float(threads))
            if i > 0:
                time.sleep(spacing)
            agent = LoadAgent(interval, self.msg, self.start_time)
            agent.setDaemon(True)
            print 'starting thread # %i' % i
            agent.start()
        while True:
            time.sleep(.25)



class LoadAgent(Thread):
    lock = Lock()

    def __init__(self, interval, msg, start_time):
        Thread.__init__(self)
        self.interval = interval
        self.msg = msg
        self.start_time = start_time
        
        # choose timer to use
        if sys.platform.startswith('win'):
            self.default_timer = time.clock
        else:
            self.default_timer = time.time
            
            
    def run(self):
        while True:
            start = self.default_timer()               
            try:
                self.send(self.msg)
            except:
                print 'request failed'
            finish = self.default_timer()
            latency = (finish - start)
            expire_time = (self.interval - latency)
            self.write_result(latency, self.start_time)   
            if expire_time > 0:
                time.sleep(expire_time)
              
  
    def send(self, msg):
        if USE_SSL:
            conn = httplib.HTTPSConnection(msg[0])
        else:
            conn = httplib.HTTPConnection(msg[0])
        try:
            #conn.set_debuglevel(1)
            conn.request('GET', msg[1])
            resp = conn.getresponse().read()
        finally:
            conn.close()
        

    def write_result(self, latency, start_time):
        self.lock.acquire()
        try:
            f = open('results.csv', 'a')
            elapsed = (time.time() - start_time)
            f.write('%.3f,%.3f\n' % (elapsed, latency))
            f.flush()
            f.close()
        finally:
            self.lock.release()
        print '%.3f' % latency
        
        

if __name__ == '__main__':
    main()