#!/usr/bin/env python
#  (c) Corey Goldberg (corey@goldb.org) 2008-2009
#
#  Get health metrics from a Windows server with WMI


import wmi
import re
from subprocess import Popen, PIPE



class MetricsFetcher:
    def __init__(self, computer, user, password):
        self.c = wmi.WMI(find_classes=False, computer=computer, user=user, password=password)    
        
    def get_uptime(self):
        secs_up = int([uptime.SystemUpTime for uptime in 
            self.c.Win32_PerfFormattedData_PerfOS_System()][0])
        hours_up = secs_up / 3600
        return hours_up

    def get_cpu(self):
        utilizations = [cpu.LoadPercentage for cpu in self.c.Win32_Processor()]
        utilization = int(sum(utilizations) / len(utilizations))  # avg all cores/processors
        return utilization
        
    def get_mem_mbytes(self):
        available_mbytes = int([mem.AvailableMBytes for mem in 
            self.c.Win32_PerfFormattedData_PerfOS_Memory()][0])
        return available_mbytes

    def get_mem_pct(self):
        pct_in_use = int([mem.PercentCommittedBytesInUse for mem in 
            self.c.Win32_PerfFormattedData_PerfOS_Memory()][0])
        return pct_in_use        

    def get_disk_used_pct(self, drive):
        for disk in self.c.Win32_LogicalDisk(Name=drive):
            total = long(disk.Size) / 1073741824.0
        for disk in self.c.Win32_LogicalDisk(Name=drive):
            free = long(disk.FreeSpace) / 1073741824.0
        used = total - free
        pct_used = int((used * 100) / total)
        return pct_used
        
    def get_disk_non_idle_pct(self, drive):
        pct_non_idle = 100 - (int([disk.PercentIdleTime for disk in 
            self.c.Win32_PerfFormattedData_PerfDisk_LogicalDisk(Name=drive)][0]))
        return pct_non_idle
        
      

def ping(host_name):
    p = Popen('ping -n 1 ' + host_name, stdout=PIPE)
    m = re.search('Average = (.*)ms', p.stdout.read())
    if m:
        return True
    else:
        raise Exception  


