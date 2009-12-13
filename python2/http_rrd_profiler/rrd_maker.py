#!/usr/bin/env python
# Corey Goldberg - Dec 2009


import rrd

interval = 5  # insertion interval, secs

my_rrd = rrd.RRD('http_latency.rrd')
my_rrd.create_rrd(interval)

