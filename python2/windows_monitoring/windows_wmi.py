#!/usr/bin/env python
#
#  Corey Goldberg - 2008
#


import re
import wmi
from subprocess import Popen, PIPE



def get_uptime(computer, user, password):
    c = wmi.WMI(computer=computer, user=user, password=password, find_classes=False)
    secs_up = int([uptime.SystemUpTime for uptime in c.Win32_PerfFormattedData_PerfOS_System()][0])
    hours_up = secs_up / 3600
    return hours_up


def get_cpu(computer, user, password):
    c = wmi.WMI(computer=computer, user=user, password=password, find_classes=False)
    utilizations = [cpu.LoadPercentage for cpu in c.Win32_Processor()]
    utilization = int(sum(utilizations) / len(utilizations))  # avg all cores/processors
    return utilization

    
def get_mem_mbytes(computer, user, password):
    c = wmi.WMI(computer=computer, user=user, password=password, find_classes=False)
    available_mbytes = int([mem.AvailableMBytes for mem in c.Win32_PerfFormattedData_PerfOS_Memory()][0])
    return available_mbytes


def get_mem_pct(computer, user, password):
    c = wmi.WMI(computer=computer, user=user, password=password, find_classes=False)
    pct_in_use = int([mem.PercentCommittedBytesInUse for mem in c.Win32_PerfFormattedData_PerfOS_Memory()][0])
    return pct_in_use
    
    
def ping(host_name):
    p = Popen('ping -n 1 ' + host_name, stdout=PIPE)
    m = re.search('Average = (.*)ms', p.stdout.read())
    if m:
        return True
    else:
        raise Exception  