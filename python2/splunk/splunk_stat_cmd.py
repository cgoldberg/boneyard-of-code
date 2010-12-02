#  
#  splunk_stat_cmd.py - search splunk for stats - command line tool
#
#  Corey Goldberg - 2010
# 
#  (tested with splunk version 4.14 (contains python 2.6.4))
#
#
#
#  instructions:
#   - save script into splunk's "bin" directory
#     (usually "/opt/splunk/bin" or "C:\Program Files\Splunk\bin")
#   - go to the "bin" directory on the command line and run: 
#     splunk cmd python splunk_stat_cmd.py <stat_name> <host> [earliest_time]
#
#
#
#  available stats:
#   - cpu_pct
#   - mem_used_pct
#   - disk_used_pct
#
#
#
#  sample invocation (default 3 minute timespan):
#  splunk cmd python splunk_stat_cmd.py cpu_util_pct myserver
#
#  sample output:
#  cpu_util_pct myserver 2010-12-01T16:51:20-0500 9.58
#
#
#
#  sample invocation (30 minute timespan):
#  splunk cmd python splunk_stat_cmd.py disk_used_pct myserver -30m
#
#  sample output:
#  disk_used_pct myserver 2010-12-01T16:12:20-0500 18
#
#
#
#  sample invocation (0 minute timespan - forced error):
#  splunk cmd python splunk_stat_cmd.py disk_used_pct myserver -0m
#
#  sample output:
#  disk_used_pct myserver - NODATA
#



import sys
import time
import splunk.auth
import splunk.search



SPLUNK_SERVER = 'localhost'
USER_NAME = 'foo'
PASSWORD = 'foo'



def main():
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)
    if len(sys.argv) == 3:
        stat_name = sys.argv[1]
        host = sys.argv[2]
        timespan = '-3m'
    if len(sys.argv) == 4:
        stat_name = sys.argv[1]
        host = sys.argv[2]
        timespan = sys.argv[3]
        
    splunk.auth.getSessionKey(USER_NAME, PASSWORD, hostPath='https://%s:8089' % SPLUNK_SERVER)
     
    if stat_name == 'cpu_pct':
        now, value = cpu_pct(host, timespan)
    elif stat_name == 'mem_used_pct':
        now, value = mem_used_pct(host, timespan)
    elif stat_name == 'disk_used_pct':
        now, value = disk_used_pct(host, timespan)
    else:
        now = '-' 
        value = 'NODATA' 
    
    print stat_name, host, now, value 
    
    

def cpu_pct(host, timespan):
    sourcetype = 'cpu'
    try:
        latest_result = get_latest_result(host, sourcetype, timespan)
        now = latest_result.time
        line = str(latest_result).split('\n')[1]
        value = 100.0 - float(line.split()[-1])
    except Exception as e:
        now = '-'
        value = str(e)
        
    return (now, value)
    
    

def mem_used_pct(host, timespan):
    sourcetype = 'vmstat'
    try:
        latest_result = get_latest_result(host, sourcetype, timespan)
        now = latest_result.time
        line = str(latest_result).split('\n')[1]
        value = line.split()[4]
    except Exception as e:
        now = '-'
        value = str(e)

    return (now, value)
    
    

def disk_used_pct(host, timespan):
    sourcetype = 'df'
    try:
        latest_result = get_latest_result(host, sourcetype, timespan)
        now = latest_result.time
        line = str(latest_result).split('\n')[1]
        value = line.split()[-2].replace('%', '')
    except Exception as e:
        now = '-'
        value = str(e)
    
    return (now, value)



def get_latest_result(host, sourcetype, timespan):
    search = 'search index="os" host="%s" sourcetype="%s"' % (host, sourcetype)
    
    try:
        job = splunk.search.dispatch(search, earliest_time=timespan, hostPath='https://%s:8089' % SPLUNK_SERVER)
    except splunk.SearchException:
        raise Exception('NODATA')
    
    while not job.isDone:
        time.sleep(.25)
          
    try:
        last_result = job.results[0]
    except IndexError:
        raise Exception('NODATA')
    
    return last_result



def usage():
    prog_name = sys.argv[0]
    print '\n%s\n\n' % prog_name
    print 'usage:'
    print '  %s <stat_name> <host> [timespan]\n' % prog_name
    print 'example:'
    print '  splunk cmd python %s cpu_util_pct myserver\n' % prog_name
    print 'example:'
    print '  splunk cmd python %s cpu_util_pct myserver -5m\n\n' % prog_name
    print 'available stats: '
    print '  cpu_pct'
    print '  mem_used_pct'
    print '  disk_used_pct'
    print



if __name__== '__main__':
    main()

