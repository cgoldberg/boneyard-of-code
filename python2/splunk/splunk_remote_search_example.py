#!/usr/bin/env python
# Corey Goldberg - 2010
# 
#  search a remote splunk server
#
#  instructions:
#   - save script into Splunk's "bin" directory
#     (usually "/opt/splunk/bin" or "C:\Program Files\Splunk\bin")
#   - go to the "bin" directory and run: 
#     $ splunk cmd python my_script.py
#



import time
import splunk.auth
import splunk.search



SPLUNK_SERVER = '192.168.12.173'
USER_NAME = 'foo'
PASSWORD = 'secret'
SEARCH_STRING = 'search *'
EARLIEST_TIME = '-15m'



def main():
    key = splunk.auth.getSessionKey(USER_NAME, PASSWORD, hostPath='https://%s:8089' % SPLUNK_SERVER)
    print 'auth key:\n%s' % key

    job = splunk.search.dispatch(SEARCH_STRING, earliest_time=EARLIEST_TIME, hostPath='https://%s:8089' % SPLUNK_SERVER)
    print 'job details:\n%s' % job

    # wait for results
    while not job.isDone:
        time.sleep(.25)
    
    print 'results:\n%s' % job    
    for result in job.results:
        print result
          
          

if __name__== '__main__':
    main()
