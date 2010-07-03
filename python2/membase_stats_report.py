#!/usr/bin/env python
# Corey Goldberg - 2010
# print a stats report from membase key-value database (membase.org)
# requires python-memcached


import memcache


mc = memcache.Client(['127.0.0.1:11211'])


for node_stats in mc.get_stats():
    server, stats = node_stats
    print server.rjust(30)
    print '--------------------------'.rjust(30), '--------------'.rjust(15)
    for stat_name, value in sorted(stats.iteritems()):
        if not stat_name.startswith('ep'):
            if not stat_name in ('libevent', 'version'):
                print stat_name.rjust(30), value.rjust(15)
    print '--------------------------'.rjust(30), '--------------'.rjust(15)
    for stat_name, value in sorted(stats.iteritems()):
        if stat_name.startswith('ep'):
            if not stat_name == 'ep_dbname':
                print stat_name.rjust(30), value.rjust(15)
                