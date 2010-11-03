#!/usr/bin/env python
# (c) Corey Goldberg (corey@goldb.org) 2009


import time
import threading
import pythoncom
import machine_stats



# set these to a Windows login with admin privileges
USER_NAME = ''
PASSWORD = ''
        
        
        
def main():           
    print 'Host,Epoch Time (secs),Uptime (hrs),CPU Utilization (%),Memory Available (MB),Memory Usage (%)'
    
    host_names = [line.strip() for line in open('machines.txt', 'r').readlines()]
    metric_store = MetricStore()
    
    # gather metrics in threads
    thread_refs = []
    for host in host_names:
        mp = MetricsProbe(host, metric_store)
        mp.start()
        thread_refs.append(mp)
        
    # wait for threads to finish    
    for t in thread_refs:
        t.join()
    


class MetricsProbe(threading.Thread):
    def __init__(self, host, metric_store):
        threading.Thread.__init__(self)
        self.host = host
        self.metric_store = metric_store
        
    def run(self):
        pythoncom.CoInitialize()  # need this for multithreading COM/WMI
        epoch_secs = int(time.time())
        try:
            mf = machine_stats.MetricsFetcher(self.host, USER_NAME, PASSWORD)
            uptime = mf.get_uptime()
            cpu = mf.get_cpu()
            mem_mb_avail = mf.get_mem_mbytes()
            mem_pct = mf.get_mem_pct()            
        except Exception, e:
            uptime = 0
            cpu = 0
            mem_mb_avail = 0
            mem_pct = 0
            print 'Error getting stats from host %s: %s' % (self.host, e)
        self.metric_store.uptimes[self.host] = uptime
        self.metric_store.cpus[self.host] = cpu
        self.metric_store.mem_mb_avails[self.host] = mem_mb_avail
        self.metric_store.mem_pcts[self.host] = mem_pct
        print '%s,%d,%d,%d,%d,%d' % (self.host, epoch_secs, uptime, cpu, mem_mb_avail, mem_pct)
                


class MetricStore(object):
    def __init__(self):
        self.uptimes = {}
        self.cpus = {}
        self.mem_mb_avails = {}
        self.mem_pcts = {}
            


if __name__ == '__main__':
    main()
