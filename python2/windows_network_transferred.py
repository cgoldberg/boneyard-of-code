#!/usr/bin/env python
#  Corey Goldberg - 2010
#  Windows: get network stats (bytes transferred)


import subprocess


def main():
    rx_bytes, tx_bytes = net_stats('eth0')
    
    print '%s bytes received' % rx_bytes
    print '%s bytes sent' % tx_bytes
    
    print '%s bits received' % (rx_bytes * 8)
    print '%s bits sent' % (tx_bytes * 8)    
    
    
    
def net_stats(interface):
    output = subprocess.Popen(['net', 'statistics', 'workstation'], stdout=subprocess.PIPE).communicate()[0]
    for line in output.splitlines():
        if 'Bytes received' in line:
            rx_bytes = int(line.split()[2])
        if 'Bytes transmitted' in line:
            tx_bytes = int(line.split()[2])
    return rx_bytes, tx_bytes   



if __name__ == '__main__':
    main()