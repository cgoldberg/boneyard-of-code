#!/usr/bin/env python
# Corey Goldberg - 2010
# print a stats report from membase key-value database (membase.org)
# requires python-memcached


import memcache


HOST = '127.0.0.1'

mc = memcache.Client(['%s:11211' % HOST])

for node_stats in mc.get_stats():
    server, stats = node_stats
    print server
    print '--------------------------'.ljust(25), '--------------'.rjust(15)
    for stat_name, value in sorted(stats.iteritems()):
        if not stat_name.startswith('ep'):
            if stat_name not in ('libevent', 'version'):
                print stat_name.ljust(25), value.rjust(15)
    print '--------------------------'.ljust(25), '--------------'.rjust(15)
    for stat_name, value in sorted(stats.iteritems()):
        if stat_name.startswith('ep'):
            if stat_name not in ('ep_dbname', 'ep_version'):
                print stat_name.ljust(25), value.rjust(15)
                
                
                

# sample output:
# 
# >python membase_stats_report.py
# 127.0.0.1:11211 (1)
# --------------------------  --------------
# auth_cmds                               0
# auth_errors                             0
# bytes_read                       81754885
# bytes_written                    77239947
# cas_badval                              0
# cas_hits                                0
# cas_misses                              0
# cmd_flush                               1
# cmd_get                            370229
# cmd_set                            380230
# conn_yields                             0
# connection_structures                  16
# curr_connections                       16
# curr_items                         178679
# daemon_connections                     10
# decr_hits                               0
# decr_misses                             0
# delete_hits                             0
# delete_misses                           0
# get_hits                           370228
# get_misses                              1
# incr_hits                               0
# incr_misses                             0
# limit_maxbytes                   67108864
# mem_used                         40909042
# pid                                  2009
# pointer_size                           64
# rejected_conns                          0
# rusage_system                   65.660000
# rusage_user                    113.320000
# threads                                 4
# time                           1278257466
# total_connections                      16
# uptime                                592
# --------------------------  --------------
# ep_commit_time                          1
# ep_data_age                           286
# ep_data_age_highwat                   286
# ep_dbinit                               0
# ep_flush_duration                       1
# ep_flush_duration_highwat               2
# ep_flusher_state                  running
# ep_flusher_todo                       483
# ep_item_commit_failed                   0
# ep_item_flush_failed                    0
# ep_max_txn_size                     50000
# ep_min_data_age                         1
# ep_queue_age_cap                        5
# ep_queue_size                      176786
# ep_storage_age                        286
# ep_storage_age_highwat                286
# ep_tap_keepalive                        0
# ep_tap_total_fetched                    0
# ep_tap_total_queue                      0
# ep_too_old                           1410
# ep_too_young                        56372
# ep_total_enqueued                  380487
# ep_total_persisted                 198703
# ep_warmed_up                       479990
# ep_warmup                            true
# ep_warmup_thread                 complete
# ep_warmup_time                          4
