#!/usr/bin/env python
# Corey Goldberg - 2010

# works with Linux 2.6.x
# requires Python 2.6+


import time


   
def disk_busy(device, sample_duration=1):
    """Return disk busy percent."""
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



def disk_reads_writes(device, sample_duration=1):
    """Return number of (reads, writes) during the sample_duration."""
    with open('/proc/diskstats') as f1:
        with open('/proc/diskstats') as f2:
            content1 = f1.read()
            time.sleep(sample_duration)
            content2 = f2.read()
    sep = '%s ' % device
    for line in content1.splitlines():
        if sep in line:
            fields = line.strip().split(sep)[1].split()
            num_reads1 = fields[0]
            num_writes1 = fields[4]
            break
    for line in content2.splitlines():
        if sep in line:
            fields = line.strip().split(sep)[1].split()
            num_reads2 = fields[0]
            num_writes2 = fields[4]
            break            
    num_reads = int(num_reads2) - int(num_reads1)
    num_writes = int(num_writes2) - int(num_writes1)    
    return num_reads, num_writes
    


if __name__ == '__main__':  
    print 'busy: %s%%' % disk_busy('sda', 5)
    r, w = disk_reads_writes('sda', 5)
    print 'reads: %s' % r
    print 'writes: %s' % w

