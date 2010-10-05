#!/usr/bin/env python
# Corey Goldberg - 2010

# works with Linux 2.6.x
# requires Python 2.6+


   
def mem_stats():
    with open('/proc/meminfo') as f:
        for line in f:
            if line.startswith('MemTotal:'):
                mem_total = int(line.split()[1]) * 1024
            if line.startswith('MemFree:'):
                mem_used = mem_total - (int(line.split()[1]) * 1024)
    return mem_used, mem_total
    
    



if __name__ == '__main__':  
    
    print mem_stats()
    

