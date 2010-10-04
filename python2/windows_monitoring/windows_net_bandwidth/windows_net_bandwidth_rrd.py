#!/usr/bin/env python
#
#  Corey Goldberg - 2010
#
#  windows_net_bandwidth_rrd.py - local network bandwidth monitoring script for windows
#
#    - monitors and graphs bandwidth utilization (throughput in/out)
#    - stores data in RRD (round-robin database)
#    - generates .png images of plots/stats
#    - run this script at regular intervals with a task/job scheduler
#    - requires python 2.x, python-wmi, rrdtool
#   
#    stats collected:
#      - net_bps_in: network throughput (bps in)
#      - net_bps_out: network throughput (bps out)
#
#    instructions:
#      - configure the script's settings:
#          - INTERVAL: collection interval in secs (how often the script is run)
#          - GRAPH_MINS: timespans for graph/png files
#          - GRAPH_DIR:  output directory
#            (* make sure the output directory is writable)
#      - add a scheduled task to windows task scheduler, to run it every INTERVAL
#



import os.path
import socket
import subprocess
import time

import wmi  # http://timgolden.me.uk/python/wmi



# Config Settings
INTERVAL = 300  # 5 mins
GRAPH_MINS = (240, 1440, 10080)  # 4hours, 1day, 1week
GRAPH_DIR = './'



def main():  
    c = wmi.WMI(computer='localhost')
    
    rx_bits = net_bits_in(c)
    tx_bits = net_bits_out(c)
    
    localhost_name = socket.gethostname()
    
    # store values in rrd and update graphs
    rrd_ops('net_bps_in', rx_bits, 'DERIVE', '009900', localhost_name, 1000)
    rrd_ops('net_bps_out', tx_bits, 'DERIVE', '000099', localhost_name, 1000)
    

def net_bits_in(c):
    rx_bytes = sum([int(net_interface.BytesReceivedPerSec) for net_interface in c.Win32_PerfRawData_Tcpip_NetworkInterface()])
    rx_bits = rx_bytes * 8
    return rx_bits
    
    
def net_bits_out(c):
    tx_bytes = sum([int(net_interface.BytesSentPerSec) for net_interface in c.Win32_PerfRawData_Tcpip_NetworkInterface()])
    tx_bits = tx_bytes * 8
    return tx_bits
        
            
def rrd_ops(stat, value, ds_type, color, title, base):
    rrd_name = '%s.rrd' % stat
    rrd = RRD(rrd_name, stat)
    rrd.base = base
    rrd.graph_title = title
    rrd.graph_color = color
    rrd.graph_dir = GRAPH_DIR
    if not os.path.exists(rrd_name):
        rrd.create(INTERVAL, ds_type)
    rrd.update(value)
    for mins in GRAPH_MINS:
        rrd.graph(mins)
    print time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()), stat, value




class RRD(object):
    def __init__(self, rrd_name, stat):
        self.stat = stat
        self.rrd_name = rrd_name
        self.rrd_exe = 'rrdtool'
        self.base = 1000  # for traffic measurement, 1 kb/s is 1000 b/s.  for sizing, 1 kb is 1024 bytes. 
        self.graph_title = ''
        self.graph_dir = '' 
        self.graph_color = 'FF6666'
        self.graph_width = 480
        self.graph_height = 160
        

    def create(self, interval, ds_type='GAUGE'):  
        interval = str(interval) 
        interval_mins = float(interval) / 60  
        heartbeat = str(int(interval) * 2)
        ds_string = ' DS:ds:%s:%s:0:U' % (ds_type, heartbeat)
        cmd_create = ''.join((self.rrd_exe, 
            ' create ', self.rrd_name, ' --step ', interval, ds_string,
            ' RRA:AVERAGE:0.5:1:', str(int(4000 / interval_mins)),
            ' RRA:AVERAGE:0.5:', str(int(30 / interval_mins)), ':800',
            ' RRA:AVERAGE:0.5:', str(int(120 / interval_mins)), ':800',
            ' RRA:AVERAGE:0.5:', str(int(1440 / interval_mins)), ':800'))
        cmd_args = cmd_create.split(' ')
        p = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        cmd_output = p.stdout.read()
        if len(cmd_output) > 0:
            raise RRDError('unable to create RRD: %s' % cmd_output.rstrip())
        
  
    def update(self, value):
        cmd_update = '%s update %s N:%s' % (self.rrd_exe, self.rrd_name, value)
        cmd_args = cmd_update.split(' ')
        p = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        cmd_output = p.stdout.read()
        if len(cmd_output) > 0:
            raise RRDError('unable to update RRD: %s' % cmd_output.rstrip())
    
    
    def graph(self, mins):       
        start_time = 'now-%s' % (mins * 60)  
        output_filename = '%s_%i.png' % (self.rrd_name, mins)
        end_time = 'now'
        cur_date = time.strftime('%m/%d/%Y %H\:%M\:%S', time.localtime())    
        cmd = [self.rrd_exe, 'graph', self.graph_dir + output_filename]
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:%s    ' % cur_date)
        cmd.append('DEF:ds=%s:ds:AVERAGE' % self.rrd_name)
        cmd.append('AREA:ds#%s:%s  ' % (self.graph_color, self.stat))
        cmd.append('VDEF:dslast=ds,LAST')
        cmd.append('VDEF:dsavg=ds,AVERAGE')
        cmd.append('VDEF:dsmin=ds,MINIMUM')
        cmd.append('VDEF:dsmax=ds,MAXIMUM')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        cmd.append('GPRINT:dslast:last %.1lf%S    ') 
        cmd.append('GPRINT:dsavg:avg %.1lf%S    ')
        cmd.append('GPRINT:dsmin:min %.1lf%S    ')
        cmd.append('GPRINT:dsmax:max %.1lf%S    ')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        cmd.append('--title=%s' % self.graph_title)
        cmd.append('--vertical-label=%s' % self.stat)
        cmd.append('--start=%s' % start_time)
        cmd.append('--end=%s' % end_time)
        cmd.append('--width=%i' % self.graph_width)
        cmd.append('--height=%i' % self.graph_height)
        cmd.append('--base=%i' % self.base)
        cmd.append('--slope-mode')
        cmd.append('--lower-limit=0')
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        cmd_output = p.stdout.read()
        if len(cmd_output) > 10:
            raise RRDError('unable to graph RRD: %s' % cmd_output.rstrip())
            
          
          
class RRDError(Exception): pass

    
    
if __name__ == '__main__':
    main()