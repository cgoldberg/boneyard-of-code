#!/usr/bin/env python
# Corey Goldberg - 2008


import urllib
import re


ip_addresses = (
    '165.123.243.168',
    '204.69.182.1',
    '147.140.233.16',
    '71.224.205.95',
    '70.91.27.53',
)


print """
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#"
    xmlns:ymaps="http://api.maps.yahoo.com/Maps/V1/AnnotatedMaps.xsd">
<channel>
"""


for ip in ip_addresses:
    response = urllib.urlopen('http://api.hostip.info/get_html.php?ip=%s' % ip).read()
    m = re.search('City: (.*)', response)
    if m:
        citystate = m.group(1)
    xml_item = """
      <item> 
        <title>%s</title>
        <ymaps:CityState>%s</ymaps:CityState>
      </item>
    """ % (ip, citystate)
    
    print xml_item
    
print """
</channel>
</rss>
"""