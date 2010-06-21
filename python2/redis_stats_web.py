#!/usr/bin/env python
# Corey Goldberg - 2010
#
# display info/stats from redis server (using python redis client) in a web page
# to access: run this script then visit http://<your_server>/stats


import redis
import BaseHTTPServer


WEB_PORT = 8081

REDIS_HOST = 'host.foo.com'
REDIS_PORT = 6379
REDIS_DB = 0


class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stats':
            self.send_response(200)
            self.end_headers()
            info = self.get_stats() 
            output = self.format_output(info)
            self.wfile.write(output)
        else: 
            self.send_error(404)
            
    def get_stats(self):
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        info = r.info()
        return info
        
    def format_output(self, info):
        output = '<html><body><table>'
        for stat, value in sorted(info.items()):
            output += '<tr><td style="font-size: 11px; font-family: monospace;">%s</td>' \
            '<td style="font-size: 11px; font-family: monospace;">%s</td></tr>' % (stat, value)
        output += '<table></body></html>'
        return output
        
        
server = BaseHTTPServer.HTTPServer(('',WEB_PORT), WebRequestHandler)
server.serve_forever()
