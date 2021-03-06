#!/usr/bin/env python
#  Corey Goldberg - 2010
#    - monitors and graphs stats from a memcached or membase node
#    - stores data in RRD (round-robin database)
#    - generates .png images of plots/stats
#    - run this script at regular intervals with a task/job scheduler
#    - requires python 2.x, python-memcached, rrdtool



import memcache
import os.path
import socket
import subprocess
import sys
import time



# Config Settings
HOST = '192.168.12.171' 
PORT = '11211'
INTERVAL = 60  # secs
GRAPH_MINS = (60, 240, 1440)  # timespans for graph/png files
GRAPH_DIR = '/var/www/membase_stats/'  # output directory



def main():
    try:
        mc = memcache.Client(('%s:%s' % (HOST, PORT),))
        all_stats = mc.get_stats()
    except Exception:
        print time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()), 'error'
        sys.exit(1)
    
    node_stats = all_stats[0][1]
    
    localhost_name = socket.gethostname()
    
    
    # set/get a test key to measure latency
    key = 'test_key_%s' % HOST
    data = '*' * 30000  # 30kb value
    
    start_timer = time.time()
    mc.set(key, data)
    stop_timer = time.time()
    set_latency_ms = (stop_timer - start_timer) * 1000

    start_timer = time.time()
    mc.get(key)
    stop_timer = time.time()
    get_latency_ms = (stop_timer - start_timer) * 1000


    # store values in rrd and update graphs
    rrd_ops('membase_curr_items', node_stats['curr_items'], 'GAUGE', 'FF9933', localhost_name, 1000)
    rrd_ops('membase_mem_used', node_stats['mem_used'], 'GAUGE', '00FF00', localhost_name, 1024)
    rrd_ops('membase_bytes_read', node_stats['bytes_read'], 'DERIVE', '6666FF', localhost_name, 1024)
    rrd_ops('membase_bytes_written', node_stats['bytes_written'], 'DERIVE', '000099', localhost_name, 1024)
    rrd_ops('membase_cmd_get', node_stats['cmd_get'], 'DERIVE', 'FF66FF', localhost_name, 1000)
    rrd_ops('membase_cmd_set', node_stats['cmd_set'], 'DERIVE', '990099', localhost_name, 1000)
    rrd_ops('membase_set_latency', set_latency_ms, 'GAUGE', '66FFFF', localhost_name, 1000)
    rrd_ops('membase_get_latency', get_latency_ms, 'GAUGE', '009999', localhost_name, 1000)
    

        
def rrd_ops(stat, value, ds_type, color, title, base, upper_limit=None):
    rrd_name = '%s.rrd' % stat
    rrd = RRD(rrd_name, stat)
    rrd.upper_limit = upper_limit
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
        self.upper_limit = None
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
        p = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        cmd_output = p.stdout.read()
        if len(cmd_output) > 0:
            raise RRDError('unable to create RRD: %s' % cmd_output.rstrip())
        
  
    def update(self, value):
        cmd_update = '%s update %s N:%s' % (self.rrd_exe, self.rrd_name, value)
        cmd_args = cmd_update.split(' ')
        p = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
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
        if self.upper_limit is not None:
            cmd.append('--upper-limit=%i' % self.upper_limit)
        cmd.append('--lower-limit=0')
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        cmd_output = p.stdout.read()
        if len(cmd_output) > 10:
            raise RRDError('unable to graph RRD: %s' % cmd_output.rstrip())
            
          
          
class RRDError(Exception): pass

    
    
if __name__ == '__main__':
    main()
