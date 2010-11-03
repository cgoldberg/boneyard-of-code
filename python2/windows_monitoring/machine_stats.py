#!/usr/bin/env python
# (c) Corey Goldberg (corey@goldb.org) 2008
#
# see: http://coreygoldberg.blogspot.com/2008/12/python-windows-remote-metrics-script.html
#


import time
import threading
import pythoncom
import machine_stats



# set these to the Windows login name with admin privileges
user_name = 'corey'
pwd = 'secret'
        
        
        
def main():           
    host_names = [line.strip() for line in open('machines.txt', 'r').readlines()]
    metric_store = MetricStore()
               
    # gather metrics in threads
    for host in host_names:
        mp = MetricsProbe(host, metric_store)
        mp.start()
    while len(threading.enumerate()) > 1:  # wait for threads to finish
        time.sleep(.25)
    
        

class MetricsProbe(threading.Thread):
    def __init__(self, host, metric_store):
        threading.Thread.__init__(self)
        self.host = host
        self.metric_store = metric_store
        
    def run(self):
        pythoncom.CoInitialize()  # need this for multithreading COM/WMI
        try:
            uptime = machine_stats.get_uptime(self.host, user_name, pwd)
            cpu = machine_stats.get_cpu(self.host, user_name, pwd)
            mem_mbyte = machine_stats.get_mem_mbytes(self.host, user_name, pwd)
            mem_pct = machine_stats.get_mem_pct(self.host, user_name, pwd)            
        except:
            uptime = 0
            cpu = 0
            mem_mbyte = 0
            mem_pct = 0
            print 'error getting stats from host: ' + self.host
        self.metric_store.uptimes[self.host] = uptime
        self.metric_store.cpus[self.host] = cpu
        self.metric_store.mem_mbytes[self.host] = mem_mbyte
        self.metric_store.mem_pcts[self.host] = mem_pct
        print '%s,uptime:%d,cpu:%d,mem_mbyte:%d,mem_pct:%d' \
            % (self.host, uptime, cpu, mem_mbyte, mem_pct)
                


class MetricStore(object):
    def __init__(self):
        self.uptimes = {}
        self.cpus = {}
        self.mem_mbytes = {}
        self.mem_pcts = {}
            


if __name__ == '__main__':
    main()