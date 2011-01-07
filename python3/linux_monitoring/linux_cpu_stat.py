#!/usr/bin/env python3
#
#  linux_cpu_stat
#
#  Copyright (c) 2010 Corey Goldberg (http://goldb.org)
#
#  License :: OSI Approved :: MIT License (http://www.opensource.org/licenses/mit-license)
# 
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#


"""
    linux_cpu_stat - Python Module for CPU Stats on Linux
    
    - works with both Python 2.6+ and Python 3
    - requires Linux 2.6.x
    - tested on Intel 64-bit (AMD64) SMP.  your mileage may vay on other architectures
    
    
    functions:
    - cpu_times()
    - cpu_percents(sample_duration=1)
    - procs_running()
    - procs_blocked()
    - load_avg()
    - cpu_info()
"""


import time



def cpu_times():
    """Return a sequence of cpu times.

    each number in the sequence is the amount of time, measured in units 
    of USER_HZ (1/100ths of a second on most architectures), that the system
    spent in each cpu mode: (user, nice, system, idle, iowait, irq, softirq, [steal], [guest]).
    
    on SMP systems, these are aggregates of all processors/cores.
    """
    
    with open('/proc/stat') as f:
        line = f.readline()
    
    cpu_times = [int(x) for x in line.split()[1:]]
    
    return cpu_times
    
    
    
def cpu_percents(sample_duration=1):
    """Return a dictionary of usage percentages and cpu modes.
    
    elapsed cpu time samples taken at 'sample_time (seconds)' apart.
    
    cpu modes: 'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq'
    
    on SMP systems, these are aggregates of all processors/cores.
    """
    
    deltas = __cpu_time_deltas(sample_duration)
    total = sum(deltas)
    percents = [100 - (100 * (float(total - x) / total)) for x in deltas]

    return {
        'user': percents[0],
        'nice': percents[1],
        'system': percents[2],
        'idle': percents[3],
        'iowait': percents[4],
        'irq': percents[5],
        'softirq': percents[6],
    }



def procs_running():
    """Return number of processes in runnable state."""
    
    return __proc_stat('procs_running')



def procs_blocked():
    """Return number of processes blocked waiting for I/O to complete."""
    
    return __proc_stat('procs_blocked')
    


def load_avg():
    """Return a sequence of system load averages (1min, 5min, 15min).
    
    number of jobs in the run queue or waiting for disk I/O 
    averaged over 1, 5, and 15 minutes
    """
    
    with open('/proc/loadavg') as f:
        line = f.readline()
    
    load_avgs = [float(x) for x in line.split()[:3]]
    
    return load_avgs
        


def cpu_info():
    """
    """
    
    with open('/proc/cpuinfo') as f:
        cpuinfo = {}
        for line in f:
            if ':' in line:
                fields = line.replace('\t', '').strip().split(': ')
                if fields[0] not in ('processor', 'core id'):  # core specific items
                    try:
                        cpuinfo[fields[0]] = fields[1]
                    except IndexError:
                        pass
        return cpuinfo



def __cpu_time_deltas(sample_duration):
    """Return a sequence of cpu time deltas for a sample period.
    
    elapsed cpu time samples taken at 'sample_time (seconds)' apart.
    
    each value in the sequence is the amount of time, measured in units 
    of USER_HZ (1/100ths of a second on most architectures), that the system
    spent in each cpu mode: (user, nice, system, idle, iowait, irq, softirq, [steal], [guest]).
    
    on SMP systems, these are aggregates of all processors/cores.
    """
    
    with open('/proc/stat') as f1:
        with open('/proc/stat') as f2:
            line1 = f1.readline()
            time.sleep(sample_duration)
            line2 = f2.readline()
    
    deltas = [int(b) - int(a) for a, b in zip(line1.split()[1:], line2.split()[1:])]
    
    return deltas
    
    
    
def __proc_stat(stat):
    with open('/proc/stat') as f:
        for line in f:
            if line.startswith(stat):
                return int(line.split()[1])
                
                



if __name__ == '__main__':   
    import pprint

    cpu_pcts = cpu_percents()
    
    utilized = 100.0 - cpu_pcts['idle']
    
    print('cpu utilization: {0:.2f}'.format(utilized)) 
    
    print('cpu mode percents:')
    pprint.pprint(cpu_pcts)
    
    print('cpu times: {0}'.format(cpu_times()))
    
    cpu_info = cpu_info()
    
    print('cpu info:')
    pprint.pprint(cpu_info)
    
    print('num cores: {0}'.format(cpu_info['cpu cores']))
    
    print('procs running: {0}'.format(procs_running()))
    
    print('procs blocked: {0}'.format(procs_blocked()))    
    
    print('load avg: {0}'.format(load_avg()))



"""
Sample output:

cpu utilization: 4.88
cpu mode percents:
{'idle': 95.121951219512198,
 'iowait': 0.0,
 'irq': 0.0,
 'nice': 0.0,
 'softirq': 0.0,
 'system': 3.41463414634147,
 'user': 1.4634146341463463}
cpu times: [911310, 7134, 648526, 23352944, 68122, 175, 2790, 0, 0, 0]
cpu info:
{'address sizes': '36 bits physical, 48 bits virtual',
 'apicid': '1',
 'bogomips': '3989.96',
 'cache size': '2048 KB',
 'cache_alignment': '64',
 'clflush size': '64',
 'cpu MHz': '2000.000',
 'cpu cores': '2',
 'cpu family': '6',
 'cpuid level': '13',
 'flags': 'fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx lm constant_tsc arch_perfmon pebs bts rep_good aperfmperf pni dtes64 monitor ds_cpl est tm2 ssse3 cx16 xtpr pdcm sse4_1 xsave lahf_lm dts',
 'fpu': 'yes',
 'fpu_exception': 'yes',
 'initial apicid': '1',
 'model': '23',
 'model name': 'Intel(R) Core(TM)2 Duo CPU     T6400  @ 2.00GHz',
 'physical id': '0',
 'siblings': '2',
 'stepping': '10',
 'vendor_id': 'GenuineIntel',
 'wp': 'yes'}
num cores: 2
procs running: 2
procs blocked: 0
load avg: [0.84999999999999998, 0.56000000000000005, 0.38]
"""

