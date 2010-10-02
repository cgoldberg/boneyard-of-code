#!/usr/bin/env python
#  Copyright (c) 2009 Corey Goldberg (corey@goldb.org)
#
#  Queueing framework - Thread Synchronization


import time
import queue
from threading import Thread



def main():
    manager = Manager()
    manager.start()
    

class Manager:
    def __init__(self):
        self.queue = queue.Queue()       
    
    def start(self):
        qw = Sender(self.queue)
        qw.setDaemon(True)
        qw.start()
        
        qr = Receiver(self.queue)
        qr.setDaemon(True)
        qr.start()
        
        while True:
            time.sleep(0.5)


class Sender(Thread):
    def __init__(self, q):
        Thread.__init__(self)
        self.q = q
        
    def run(self):
        while True:
            for i in range(10):
                self.q.put(i)
                print('put %d on queue' % i)
                time.sleep(.25)


class Receiver(Thread):
    def __init__(self, q):
        Thread.__init__(self)
        self.q = q
    
    def run(self):
        while True:
            try:
                i = self.q.get(False)
                print('got %d from queue' % i)
            except queue.Empty:
                time.sleep(0.25)


if __name__ == '__main__':
    main()