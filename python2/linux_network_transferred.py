#!/usr/bin/env python
#  Corey Goldberg - 2010
#  linux: get network stats (bytes transferred)

import re
import subprocess


def main():
    rx_bytes, tx_bytes = net_stats('eth0')
    print '%s bytes received' % rx_bytes
    print '%s bytes sent' % tx_bytes
    
    rx_bytes, tx_bytes = net_stats_ifconfig('eth0')
    print '%s bytes received' % rx_bytes
    print '%s bytes sent' % tx_bytes
    
    
# by reading /proc

def net_stats(interface):
    for line in open('/proc/net/dev'):
        if interface in line:
            data = line.split('%s:' % interface)[1].split()
            rx_bits, tx_bits = (int(data[0]) * 8, int(data[8]) * 8)
            return (rx_bits, tx_bits)
            
            
# by parsing ifconfig output    

def net_stats_ifconfig(interface):
    output = subprocess.Popen(['ifconfig', interface], stdout=subprocess.PIPE).communicate()[0]
    rx_bytes = re.findall('RX bytes:([0-9]*) ', output)[0]
    tx_bytes = re.findall('TX bytes:([0-9]*) ', output)[0]
    return (rx_bytes, tx_bytes)
         
            
if __name__ == '__main__':
    main()