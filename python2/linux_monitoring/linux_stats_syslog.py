#!/usr/bin/env python
#
#  Corey Goldberg - 2010
#
#  linux_stats_syslog.py - local system monitoring script for linux (stats fed to syslog).
#   
#    stats collected:
#      - cpu_percent: processor utilization
#      - mem_used: physical memory usage
#      - net_bps_in: network throughput (bps in)
#      - net_bps_out: network throughput (bps out)
#      - load_avg: system load average (1 min)
#      - disk_busy_percent: disk busy doing i/o
#
#    instructions:
#      - configure the script's settings:
#          - NET_INTERFACE: device to capture network stats on
#          - DISK: storage device
#      - make the script executable:
#        $ chmod +x linux_stats_splunk.py
#



import syslog
import time



# Config Settings
NET_INTERFACE = 'eth0'
DISK = 'sda'



def main():  
    cpu_pct = cpu_util(5)
    
    mem_used, mem_total = mem_stats()
    
    rx_bits, tx_bits = net_stats(NET_INTERFACE)
    
    load_avg = load_avg_1min()
    
    disk_pct = disk_busy(DISK, 5)
    
    print 'cpu_pct="%s" mem_used="%s" rx_bits="%s" tx_bits="%s" load_avg="%s" disk_pct="%s"' % \
        (cpu_pct, mem_used, rx_bits, tx_bits, load_avg, disk_pct)
        
    syslog.syslog('cpu_pct="%s" mem_used="%s" rx_bits="%s" tx_bits="%s" load_avg="%s" disk_pct="%s"' % \
        (cpu_pct, mem_used, rx_bits, tx_bits, load_avg, disk_pct))
    
    
    
def net_stats(interface):
    for line in open('/proc/net/dev'):
        if interface in line:
            data = line.split('%s:' % interface)[1].split()
            rx_bits, tx_bits = (int(data[0]) * 8, int(data[8]) * 8)
            return (rx_bits, tx_bits)
    
    
def mem_stats():
    with open('/proc/meminfo') as f:
        for line in f:
            if line.startswith('MemTotal:'):
                mem_total = int(line.split()[1]) * 1024
            if line.startswith('MemFree:'):
                mem_used = mem_total - (int(line.split()[1]) * 1024)
    return mem_used, mem_total
    

def cpu_util(sample_duration=1):
    with open('/proc/stat') as f1:
        with open('/proc/stat') as f2:
            line1 = f1.readline()
            time.sleep(sample_duration)
            line2 = f2.readline()
    deltas = [int(b) - int(a) for a, b in zip(line1.split()[1:], line2.split()[1:])]
    idle_delta = deltas[3]
    total = sum(deltas)
    util_pct = 100 * (float(total - idle_delta) / total)
    return util_pct


def disk_busy(device, sample_duration=1):
    with open('/proc/diskstats') as f1:
        with open('/proc/diskstats') as f2:
            content1 = f1.read()
            time.sleep(sample_duration)
            content2 = f2.read()
    sep = '%s ' % device
    for line in content1.splitlines():
        if sep in line:
            io_ms1 = line.strip().split(sep)[1].split()[9]
            break
    for line in content2.splitlines():
        if sep in line:
            io_ms2 = line.strip().split(sep)[1].split()[9]
            break            
    delta = int(io_ms2) - int(io_ms1)
    total = sample_duration * 1000
    busy_pct = 100 - (100 * (float(total - delta) / total))
    return busy_pct


def load_avg_1min():
    with open('/proc/loadavg') as f:
        line = f.readline()
    load_avg = float(line.split()[0])  # 1 minute load average
    return load_avg
    
  
    
if __name__ == '__main__':
    main()