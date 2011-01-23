#!/usr/bin/env python3
#
#  Corey Goldberg - 2011
#
#  run tests via WebPageTest HTTP/XML API
#  http://www.webperformancecentral.com/wiki/WebPagetest/Automating_Pagetest
#
#
#  submit a url to WebPageTest to test a given page.
#  check for results every 30 secs.
#
#  work in progress...
#  



import time
import xml.etree.ElementTree as etree
from urllib.parse import urlencode
from urllib.request import urlopen



TEST_URL = 'http://www.example.com'
WPT_URL = 'http://www.webpagetest.org/runtest.php'



def main():
    
    test_params = {
        'url': TEST_URL,
        'f': 'xml',
        'fvonly': '1',
    }   
    
    print('submitting test...')
    submission_resp = submit_test(WPT_URL, test_params)
    print('received: ')
    print(submission_resp)
    print('\n\n')
    
    print('following xmlUrl to check test status...')
    xml_url = submission_resp['xmlUrl']
    status_code = check_status(xml_url)
    print('received:')
    print(status_code)
    print('\n\n')
    
    if status_code != 200:
        num_tries = 20
        wait_between_secs = 30
        for _ in range(num_tries):
            print('waiting %d secs...' % wait_between_secs)
            time.sleep(wait_between_secs)
            print('checking on results...')
            status_code = check_status(xml_url)
            print('received:')
            print(status_code)
            print('\n\n')
            if status_code == 200:
                break
    
    if status_code == 200:
        print('getting test results in xml format...')
        resp = urlopen(xml_url)
        xml_results = resp.read().decode('utf-8') 
        print('received:')
        print(xml_results)
        print('\n\n')
    else:
        print('no results meng')
    


def submit_test(url, test_params):
    resp = urlopen("%s?%s" % (url, urlencode(test_params)))
    xml_resp = resp.read().decode('utf-8')
    doc = etree.XML(xml_resp)
    status_code = doc.findtext('statusCode')
    response = {}
    if status_code == '200':
        for node in doc.find('data'):
            response[node.tag] = node.text
    return response



def check_status(xml_url):
    resp = urlopen(xml_url)
    xml_resp = resp.read().decode('utf-8')
    doc = etree.XML(xml_resp)
    status_code = doc.findtext('statusCode')
    return int(status_code)
        
        
        
if __name__ == '__main__':
    main()
    
    

