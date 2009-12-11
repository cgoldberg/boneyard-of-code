#!/usr/bin/env python
# Corey Goldberg - 2009


# Waterfall plot using Matplotlib
# under construction


from pylab import *



def waterfall_graph(time_lines):
    fig = figure(figsize=(8, 3))  # image dimensions  
    ax = fig.add_subplot(111)
    ax.set_xlabel('Transfer Time (millisecs)', size='x-small')
    xticks(size='xx-small')
    ax.yaxis.set_major_formatter(NullFormatter())
    #ax.set_yticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )

    for i, line in enumerate(time_lines):
        print line
        ax.plot(line, [i + 1, i + 1]) 
    
    ax.set_ylim(0, len(time_lines) + 1)
    savefig('foo.png') 
    

a = [1, 3]
b = [2, 4]
c = [3, 5]

waterfall_graph([a, b, c])