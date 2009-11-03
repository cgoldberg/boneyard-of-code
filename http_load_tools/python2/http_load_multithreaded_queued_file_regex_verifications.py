#!/usr/bin/env python
#  Copyright (c) 2008-2009 Corey Goldberg (corey@goldb.org)
#
#  Multithreaded HTTP Load Generator


import time
import sys
import os
import re
import httplib
import Queue
from threading import Thread



# URL parameters
USE_SSL = False  # HTTPS/SSL support
HOST = 'example.com'
PATH = '/'

# load parameters
THREADS = 1
INTERVAL = 0  # secs
RAMPUP = 0  # secs

# response verification
VERIFY_REGEX = '.*'



def main():
    manager = LoadManager()
    manager.msg = (HOST, PATH)
    manager.start(THREADS, INTERVAL, RAMPUP, VERIFY_REGEX)
    


class LoadManager:
    def __init__(self):
        self.msg = ('localhost', '/')
        self.start_time = time.time()
        self.q = Queue.Queue()       
    

    def start(self, threads=1, interval=0, rampup=0, verify_regex='.*'):
        try:
            os.remove('results.csv')
        except:
            pass
        
        # start the thread for reading and writing queued results
        rw = ResultWriter(self.q, self.start_time)
        rw.setDaemon(True)
        rw.start()
        
        # start the agent threads
        for i in range(threads):
            spacing = (float(rampup) / float(threads))
            if i > 0:
                time.sleep(spacing)
            agent = LoadAgent(self.q, interval, self.msg, verify_regex, self.start_time)
            agent.setDaemon(True)
            print 'starting thread # %i' % i
            agent.start()
        while True:
            time.sleep(.25)



class LoadAgent(Thread):
    def __init__(self, q, interval, msg, verify_regex, start_time):
        Thread.__init__(self)
        self.interval = interval
        self.msg = msg
        self.verify_regex = verify_regex
        self.compiled_verify_regex = re.compile(verify_regex)
        self.start_time = start_time
        self.q = q
        
        # choose timer to use
        if sys.platform.startswith('win'):
            self.default_timer = time.clock
        else:
            self.default_timer = time.time
            

    def run(self):
        while True:
            start = self.default_timer()
            try:
                resp_body, resp_code = self.__send(self.msg)
                finish = self.default_timer()
                self.__verify(resp_body, resp_code, self.compiled_verify_regex)
                verify_passed = 'PASSED'
            except Exception, e:
                print e
                finish = self.default_timer()
                verify_passed = 'FAILED'
                resp_code = 0
            latency = (finish - start)
            self.q.put((time.time(), latency, resp_code, verify_passed))
            expire_time = (self.interval - latency)   
            if expire_time > 0:
                time.sleep(expire_time)
                

    def __send(self, msg):
        if USE_SSL:
            conn = httplib.HTTPSConnection(msg[0])
        else:
            conn = httplib.HTTPConnection(msg[0])
        try:
            #conn.set_debuglevel(1)
            conn.request('GET', msg[1])
            resp = conn.getresponse()
            resp_body = resp.read()
            resp_code = resp.status
        except Exception, e:
            raise Exception('Connection Error: %s' % e)
        finally:
            conn.close()
        return (resp_body, resp_code)
    

    def __verify(self, resp_body, resp_code, compiled_verify_regex):
        if resp_code >= 400:
            raise ValueError('Response Error: HTTP %d Response' % resp_code)
        if not re.search(compiled_verify_regex, resp_body):
            raise Exception('Verification Error: Regex Did Not Match Response')
        return True      



class ResultWriter(Thread):
    def __init__(self, q, start_time):
        Thread.__init__(self)
        self.q = q
        self.start_time = start_time
    

    def run(self):
        f = open('results.csv', 'a')
        while True:
            try:
                q_tuple = self.q.get(False)
                trans_end_time, latency, resp_code, verify_passed = q_tuple
                elapsed = (trans_end_time - self.start_time)
                f.write('%.3f,%.3f,%i,%s\n' % (elapsed, latency, resp_code, verify_passed))
                f.flush()
                print '%.3f' % latency
            except Queue.Empty:
                # re-check queue for messages every x sec
                time.sleep(.25)



if __name__ == '__main__':
    main()