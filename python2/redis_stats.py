#!/usr/bin/env python
# Corey Goldberg - 2010
# print info/stats from redis server (using python redis client)


import redis

HOST = 'localhost'
PORT = 6379
DB = 0

r = redis.Redis(host=HOST, port=PORT, db=DB)
info = r.info()
for stat, value in info.iteritems():
    print stat, value
    
    
