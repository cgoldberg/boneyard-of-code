#!/usr/bin/env python


import rrd

interval = 5  # insertion interval, secs

my_rrd = rrd.RRD('http_latency.rrd')
my_rrd.create_rrd(interval)

