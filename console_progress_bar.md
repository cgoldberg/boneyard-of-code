
---


### description: ###
ascii command-line progress bar with percentage and elapsed time display

### requirements: ###
Python 3.0+

### author: ###
Corey Goldberg<br />
[goldb.org](http://goldb.org)

### progress\_bar.py source code (SVN): ###
  * view: [console\_progress\_bar.py](http://code.google.com/p/corey-projects/source/browse/trunk/python3/console_progress_bar/console_progress_bar.py)


---


### example usage: ###
```
#!/usr/bin/env python3

import console_progress_bar


# print a static progress bar:
#  [##########       25%                  ]  15s/60s

pb = console_progress_bar.ProgressBar(60)
pb.update_time(15)
print(pb)


# print a dynamic updating progress bar on one line:
#
#  [################100%##################]  10s/10s
#  done

secs = 10
pb = console_progress_bar.ProgressBar(secs)
print('\nplease wait %d seconds...\n' % secs)

# spawn asych (threads/processes/etc) code here that runs for secs.
# the call to .animate() blocks the main thread.

pb.animate(secs)

print('done')
```
### example output: ###


`$ python3 progress_bar.py`

<br />
`static progress bar:`<br />
`[##########       25%                  ]  15s/60s`

`static progress bar:`<br />
`[=================83%============      ]  25s/30s`

<br />
`dynamic updating progress bar:`

`please wait 10 seconds...`

`[################100%##################]  10s/10s`<br />
`done`


---
