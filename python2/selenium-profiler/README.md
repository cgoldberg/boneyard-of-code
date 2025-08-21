## Automated Web/HTTP Profiler with Selenium and Python

by Corey Goldberg (c) 2009, 2011

----

### What is it?

Selenium-profiler is a web/http profiler built with Selenium-RC and Python. It
profiles page load time and network traffic for a web page. The profiler uses
Selenium-RC to automate site navigation (via browser), proxy traffic, and sniff
the proxy for network traffic stats as requests pass through during a page load.

It is useful to answer questions like:
- how many http requests does that page make?
- how fast are the http responses coming back?
- which http status codes are returned?
- how many of each object type are requested?
- what is the total page load time?

### License:

GNU GPL v3
This program is Free Open Source software


### Contents:

 - `web_profiler.py`


### How do you use it?

- Install Python
- Install Java
- Download Selenium Server
- Install Selenium bindings for Python
- Run Selenium server: `java -jar selenium-server.jar`
- Run `web_profiler.py`

#### Notes:

you may need to adjust browser security settings to get it to work properly to
run against an HTTPS/SSL enabled site, you need to install a fake certificate.
Look inside `selenium-server.jar` for the cert.

#### Command Line Parameters:

```
web_profiler.py <url> [browser_launcher]
```

#### Sample usage:

```
$ python web_profiler.py www.google.com
$ python web_profiler.py http://www.google.com *firefox
```

- use `firefox` to launch Mozilla Firefox
- use `iexplore` or `iexploreproxy` to launch Internet Explorer
- use `googlechrome` to launch Google Chrome

#### Sample Output:

```
--------------------------------
results for http://www.google.com/

content size: 31.096 kb

http requests: 7
status 200: 6
status 204: 1

profiler timing:
0.344 secs (page load)
0.328 secs (network: end last request)
0.110 secs (network: end first request)

file extensions: (count, size)
gif: 1, 3.011 kb
ico: 1, 1.150 kb
js: 2, 18.083 kb
png: 1, 5.401 kb
unknown: 2, 3.451 kb

http timing detail: (status, method, doc, size, time)
204, GET, /generate_204, 0, 62 ms
200, GET, /favicon.ico, 1150, 31 ms
200, GET, /barcode09.gif, 3011, 31 ms
200, GET, /, 3451, 110 ms
200, GET, /2cca7b2e99206b9c.js, 3451, 78 ms
200, GET, /nav_logo7.png, 5401, 16 ms
200, GET, /f_wkquEsVv8.js, 14632, 47 ms
--------------------------------
```
