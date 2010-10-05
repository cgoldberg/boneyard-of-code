#!/usr/bin/env python
#
#  Corey Goldberg - 2010
#
#  linux_cpu_mode_rrd - local system monitoring script for linux
#
#    - monitors and detailed CPU statistics
#    - stores data in RRD (round-robin database)
#    - generates .png images of plots/stats
#    - run this script at regular intervals with a task/job scheduler
#    - requires python 2.x, rrdtool
#
#    instructions:
#      - configure the script's settings:
#          - INTERVAL: collection interval in secs (how often the script is run)
#          - GRAPH_MINS: timespans for graph/png files
#          - GRAPH_DIR:  output directory
#            (* make sure the output directory is writable)
#      - make the script executable:
#        $ chmod +x linux_cpu_mode_rrd.py
#      - add an entry to your crontab (crontab -e) so cron will run it.
#        example crontab entry using a 60 sec (1 min) interval:
#        */1 * * * * /home/corey/linux_cpu_mode_rrd.py
#
#    prereqs on debian/ubuntu:
#      - install rrdtool
#        $ sudo apt-get install rrdtool
#



import os.path
import socket
import subprocess
import time



# Config Settings
INTERVAL = 60  # 1 min
GRAPH_MINS = (60, 240, 1440)  # 1hour, 4hours, 1day
GRAPH_DIR = '/var/www/'



def main():  
    cpu_mode_percents = cpu_percents(5)
    print cpu_mode_percents   
    localhost_name = socket.gethostname()
    
    # store values in rrd and update graphs
    rrd_name = 'cpu_modes.rrd'
    rrd = RRD(rrd_name, 'cpu_modes')
    rrd.upper_limit = 100
    rrd.graph_title = localhost_name
    rrd.graph_dir = GRAPH_DIR
    if not os.path.exists(rrd_name):
        rrd.create(INTERVAL, 'GAUGE')
    rrd.update(cpu_mode_percents['user'], 
               cpu_mode_percents['nice'],  
               cpu_mode_percents['system'], 
               cpu_mode_percents['idle'], 
               cpu_mode_percents['iowait'],  
               cpu_mode_percents['irq'], 
               cpu_mode_percents['softirq'])
    for mins in GRAPH_MINS:
        rrd.graph(mins)
    
    

def cpu_percents(sample_duration=1):
    with open('/proc/stat') as f1:
        with open('/proc/stat') as f2:
            line1 = f1.readline()
            time.sleep(sample_duration)
            line2 = f2.readline()
    deltas = [int(b) - int(a) for a, b in zip(line1.split()[1:], line2.split()[1:])]
        
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
        self.graph_width = 680
        self.graph_height = 280
        

    def create(self, interval, ds_type='GAUGE'):  
        interval = str(interval) 
        interval_mins = float(interval) / 60  
        heartbeat = str(int(interval) * 2)
        ds_string_user = ' DS:ds_user:%s:%s:0:U' % (ds_type, heartbeat)
        ds_string_nice = ' DS:ds_nice:%s:%s:0:U' % (ds_type, heartbeat)
        ds_string_system = ' DS:ds_system:%s:%s:0:U' % (ds_type, heartbeat)
        ds_string_idle = ' DS:ds_idle:%s:%s:0:U' % (ds_type, heartbeat)
        ds_string_iowait = ' DS:ds_iowait:%s:%s:0:U' % (ds_type, heartbeat)
        ds_string_irq = ' DS:ds_irq:%s:%s:0:U' % (ds_type, heartbeat)
        ds_string_softirq = ' DS:ds_softirq:%s:%s:0:U' % (ds_type, heartbeat)
        
        cmd_create = ''.join((self.rrd_exe, 
            ' create ', self.rrd_name, ' --step ', interval, 
            ds_string_user, ds_string_nice, ds_string_system, 
            ds_string_idle, ds_string_iowait, ds_string_irq, ds_string_softirq, 
            ' RRA:AVERAGE:0.5:1:', str(int(4000 / interval_mins)),
            ' RRA:AVERAGE:0.5:', str(int(30 / interval_mins)), ':800',
            ' RRA:AVERAGE:0.5:', str(int(120 / interval_mins)), ':800',
            ' RRA:AVERAGE:0.5:', str(int(1440 / interval_mins)), ':800'))
        cmd_args = cmd_create.split(' ')
        p = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        cmd_output = p.stdout.read()
        if len(cmd_output) > 0:
            raise RRDError('unable to create RRD: %s' % cmd_output.rstrip())
        
  
    def update(self, user, nice, system, idle, iowait, irq, softirq):
        cmd_update = '%s update %s N:%i:%i:%i:%i:%i:%i:%i' % (self.rrd_exe, self.rrd_name, user, nice, system, idle, iowait, irq, softirq)
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
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:%s' % cur_date)
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:CPU Mode .....Avg Spent\\s')
        cmd.append('COMMENT:\\s')
        
        cmd.append('DEF:ds_idle=' + self.rrd_name + ':ds_idle:AVERAGE')
        cmd.append('AREA:ds_idle#CCCCCC:idle')
        cmd.append('VDEF:ds_idlelast=ds_idle,LAST')
        cmd.append('VDEF:ds_idleavg=ds_idle,AVERAGE')
        cmd.append('GPRINT:ds_idleavg:......%.2lf%%')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        
        cmd.append('DEF:ds_user=' + self.rrd_name + ':ds_user:AVERAGE')
        cmd.append('LINE:ds_user#FF0000:user')
        cmd.append('VDEF:ds_userlast=ds_user,LAST')
        cmd.append('VDEF:ds_useravg=ds_user,AVERAGE')
        cmd.append('GPRINT:ds_useravg:......%.2lf%%')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        
        cmd.append('DEF:ds_nice=' + self.rrd_name + ':ds_nice:AVERAGE')
        cmd.append('LINE:ds_nice#FF9999:nice')
        cmd.append('VDEF:ds_nicelast=ds_nice,LAST')
        cmd.append('VDEF:ds_niceavg=ds_nice,AVERAGE')
        cmd.append('GPRINT:ds_niceavg:......%.2lf%%')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        
        cmd.append('DEF:ds_system=' + self.rrd_name + ':ds_system:AVERAGE')
        cmd.append('LINE:ds_system#0000FF:system')
        cmd.append('VDEF:ds_systemlast=ds_system,LAST')
        cmd.append('VDEF:ds_systemavg=ds_system,AVERAGE')
        cmd.append('GPRINT:ds_systemavg:....%.2lf%%')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        
        cmd.append('DEF:ds_iowait=' + self.rrd_name + ':ds_iowait:AVERAGE')
        cmd.append('LINE:ds_iowait#00FF00:iowait')
        cmd.append('VDEF:ds_iowaitlast=ds_iowait,LAST')
        cmd.append('VDEF:ds_iowaitavg=ds_iowait,AVERAGE')
        cmd.append('GPRINT:ds_iowaitavg:....%.2lf%%')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        
        cmd.append('DEF:ds_irq=' + self.rrd_name + ':ds_irq:AVERAGE')
        cmd.append('LINE:ds_irq#00FFFF:irq')
        cmd.append('VDEF:ds_irqlast=ds_irq,LAST')
        cmd.append('VDEF:ds_irqavg=ds_irq,AVERAGE')
        cmd.append('GPRINT:ds_irqavg:.......%.2lf%%')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        
        cmd.append('DEF:ds_softirq=' + self.rrd_name + ':ds_softirq:AVERAGE')
        cmd.append('LINE:ds_softirq#FF9933:softirq')
        cmd.append('VDEF:ds_softirqlast=ds_softirq,LAST')
        cmd.append('VDEF:ds_softirqavg=ds_softirq,AVERAGE')
        cmd.append('GPRINT:ds_softirqavg:...%.2lf%%')
        cmd.append('COMMENT:\\s')
        cmd.append('COMMENT:\\s')
        
        cmd.append('--title=%s CPU ' % self.graph_title)
        cmd.append('--vertical-label=Utilization %')
        cmd.append('--start=%s' % start_time)
        cmd.append('--end=%s' % end_time)
        cmd.append('--width=%i' % self.graph_width)
        cmd.append('--height=%i' % self.graph_height)
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