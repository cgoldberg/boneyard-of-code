
---


## linux\_cpu\_mode\_rrd.py ##

**Corey Goldberg - 2010**


---


## Source Code (SVN) ##

  * [linux\_cpu\_mode\_rrd.py](http://code.google.com/p/corey-projects/source/browse/trunk/python2/linux_monitoring/linux_cpu_mode_rrd/linux_cpu_mode_rrd.py)
  * [linux\_cpu\_mode.html](http://code.google.com/p/corey-projects/source/browse/trunk/python2/linux_monitoring/linux_cpu_mode_rrd/linux_cpu_mode.html)


## Information ##

  * monitors detailed CPU statistics
  * stores data in RRD (round-robin database)
  * generates .png images of plots/stats
  * run this script at regular intervals with a task/job scheduler
  * requires python 2.x, rrdtool


## Instructions ##
  * configure the script's settings:
    * INTERVAL: collection interval in secs (how often the script is run)
    * GRAPH\_MINS: timespans for graph/png files
    * GRAPH\_DIR:  output directory (make sure the output directory is writable)
  * make the script executable:
```
  $ chmod +x linux_cpu_mode_rrd.py
```
  * add an entry to your crontab (crontab -e) so cron will run it.
> example crontab entry using a 60 sec (1 min) interval:
```
  */1 * * * * /home/corey/linux_cpu_mode_rrd.py
```

## Screenshot ##

![http://corey-projects.googlecode.com/svn/trunk/python2/linux_monitoring/linux_cpu_mode_rrd/2010-10-04_Screenshot_CPU_Mode_Stats.png](http://corey-projects.googlecode.com/svn/trunk/python2/linux_monitoring/linux_cpu_mode_rrd/2010-10-04_Screenshot_CPU_Mode_Stats.png)