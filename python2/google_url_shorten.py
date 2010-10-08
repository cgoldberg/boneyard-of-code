#!/usr/bin/python  
#  Corey Goldberg - 2010
#
#  shorten a URL using Google's shortening service (goo.gl)
#


import json
import urllib
import urllib2



def shorten(url):
    gurl = 'http://goo.gl/api/url?url=%s' % urllib.quote(url)
    req = urllib2.Request(gurl, data='')
    req.add_header('User-Agent', 'toolbar')
    results = json.load(urllib2.urlopen(req))
    return results['short_url']



if __name__ == '__main__':
    print shorten('http://www.goldb.org/')
    print shorten('www.yahoo.com')