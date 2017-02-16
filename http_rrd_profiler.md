## http\_rrd\_profiler ##

**Corey Goldberg - 2009, 2011**


---


## Source Code (SVN) ##

  * [http\_rrd\_profiler.py](http://code.google.com/p/corey-projects/source/browse/trunk/python2/http_rrd_profiler/http_rrd_profiler.py)
  * [rrd.py](http://code.google.com/p/corey-projects/source/browse/trunk/python2/http_rrd_profiler/rrd.py)


## Information ##

  * sends synthetic transactions (HTTP requests) to an API
  * stores response times in RRD database:
    * request sent
    * response received
    * content transferred
  * generates PNG time-series graphs from RRDs


## Requirements ##

  * Python 2 (2.5+)
  * [RRDTool](http://oss.oetiker.ch/rrdtool/)


## Screenshots ##
![http://corey-projects.googlecode.com/svn/trunk/img/http_rrd_profiler-sample1.png](http://corey-projects.googlecode.com/svn/trunk/img/http_rrd_profiler-sample1.png)<br />
![http://corey-projects.googlecode.com/svn/trunk/img/http_rrd_profiler-sample2.png](http://corey-projects.googlecode.com/svn/trunk/img/http_rrd_profiler-sample2.png)