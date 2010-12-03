#  
#  splunk_stat_cmd.py - search splunk for stats - command line tool
#
#  Corey Goldberg - 2010
# 
#  (tested with splunk 4.x (python 2.6))
#
#
#
#  instructions:
#   - save script into splunk's "bin" directory
#     (usually "/opt/splunk/bin" or "C:\Program Files\Splunk\bin")
#   - go to the "bin" directory on the command line and run: 
#     splunk cmd python splunk_stat_cmd.py <stat_name> <host> [timespan]
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
#  example usage (default 3 minute timespan):
#  > splunk cmd python splunk_stat_cmd.py cpu_pct myserver
#
#  example output:
#  cpu_util_pct myserver 2010-12-01T16:51:20-0500 9.58
#
#
#
#  example usage (30 minute timespan):
#  > splunk cmd python splunk_stat_cmd.py disk_used_pct myserver -30m
#
#  example output:
#  disk_used_pct myserver 2010-12-01T16:12:20-0500 18
#
#
#
#  example usage (0 minute timespan - forced error):
#  > splunk cmd python splunk_stat_cmd.py mem_used_pct myserver -0m
#
#  example output:
#  mem_used_pct myserver - NODATA
#



import sys
import time
import splunk.auth
import splunk.search



SPLUNK_SERVER = 'localhost'
USER_NAME = 'foo'
PASSWORD = 'foo'



def main():
    if len(sys.argv) not in (3, 4):
        usage()
        sys.exit(1)
        
    stat_name = sys.argv[1]
    host = sys.argv[2]
    
    if len(sys.argv) == 3:
        timespan = '-3m'
    else:
        timespan = sys.argv[3]
    
    
    try:    
        splunk.auth.getSessionKey(USER_NAME, PASSWORD, hostPath='https://%s:8089' % SPLUNK_SERVER)
    except Exception as e:
        now, value = ('-', str(e))
    
    
    dispatch = {
        'cpu_pct': cpu_pct,
        'mem_used_pct': mem_used_pct,
        'disk_used_pct': disk_used_pct,
    }
    
    try:
        now, value = dispatch[stat_name](host, timespan)
    except KeyError:
        now, value = ('-', 'Invalid Stat Name')
    except Exception as e:
        now, value = ('-', str(e))
        
    
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
    
    job = splunk.search.dispatch(search, earliest_time=timespan, hostPath='https://%s:8089' % SPLUNK_SERVER)
    
    while not job.isDone:
        time.sleep(.25)
          
    try:
        last_result = job.results[0]
    except IndexError:
        raise Exception('NODATA')
    
    return last_result



def usage():
    prog_name = sys.argv[0]
    print '\n %s\n\n' % prog_name
    print ' usage:'
    print '   %s <stat_name> <host> [timespan]\n' % prog_name
    print ' example:'
    print '   > splunk cmd python %s cpu_pct myserver\n' % prog_name
    print ' example:'
    print '   > splunk cmd python %s cpu_pct myserver -5m\n\n' % prog_name
    print ' available stats: '
    print '   cpu_pct'
    print '   mem_used_pct'
    print '   disk_used_pct'
    print



if __name__== '__main__':
    main()

