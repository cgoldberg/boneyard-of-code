#!/usr/bin/env python
#  Corey Goldberg - 2010
#  linux: get network stats (bytes transferred) by parsing ifconfig output

import re
import subprocess


def main():
    rx_bytes, tx_bytes = get_network_bytes('eth0')
    print '%s bytes received' % rx_bytes
    print '%s bytes sent' % tx_bytes
    
    
def get_network_bytes(interface):
    output = subprocess.Popen(['ifconfig', interface], stdout=subprocess.PIPE).communicate()[0]
    rx_bytes = re.findall('RX bytes:([0-9]*) ', output)[0]
    tx_bytes = re.findall('TX bytes:([0-9]*) ', output)[0]
    return (rx_bytes, tx_bytes)


if __name__ == '__main__':
    main()