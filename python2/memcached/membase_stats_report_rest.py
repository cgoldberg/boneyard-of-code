#!/usr/bin/env python
# Corey Goldberg - 2010
# print a 60 sec snapshot report of bucket statistics from Membase (Membase Management REST API)


import json
import urllib


HOST = '192.168.12.171'
PORT = '8080'
BUCKET = 'default'


url =  'http://%s:%s/pools/default/buckets/%s/stats?stat=opsbysecond&period=1m' % (HOST, PORT, BUCKET)

results = json.load(urllib.urlopen(url))
 
print 'stat'.rjust(23), 'min'.rjust(15), 'avg'.rjust(15), 'max'.rjust(15)
print '-----------------------------------------------------------------------'
   
for stat_name, values in sorted(results['op']['samples'].iteritems()):
    if stat_name not in ['timestamp']:
        mn = '%.0f' % min(values)
        mx = '%.0f' % max(values)
        avg = '%.2f' % (float(sum(values)) / len(values))
        print stat_name.rjust(23), mn.rjust(15), avg.rjust(15), mx.rjust(15)
        



#  Sample Output:
#  
#                     stat             min             avg             max
#  -----------------------------------------------------------------------
#               bytes_read         1101694      3131017.95         4886256
#            bytes_written           21529       291033.12          779589
#               cas_badval               0            0.00               0
#                 cas_hits               0            0.00               0
#               cas_misses               0            0.00               0
#                  cmd_get             187          382.68             563
#                  cmd_set              42          118.78             180
#         curr_connections              50           60.92              78
#               curr_items            2834         8637.61           16261
#                decr_hits               0            0.00               0
#              decr_misses               0            0.00               0
#              delete_hits               0            0.00               0
#            delete_misses               0            0.00               0
#              disk_writes              38         1416.90            3929
#          ep_flusher_todo               0          289.34            2025
#           ep_io_num_read               0            0.00               0
#            ep_queue_size              38         1127.56            3617
#                 get_hits               0           10.14              27
#               get_misses             187          372.54             542
#                incr_hits               0            0.00               0
#              incr_misses               0            0.00               0
#                 mem_used        87788498    161517318.25       259170453
#                   misses             187          372.54             542
#                      ops             229          501.46             737
#                  updates              42          118.78             180