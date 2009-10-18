

from collections import defaultdict


class Series(object):
    def __init__(self, points, interval):
        # points is a list of tuples: (sec, value)
        # interval is in secs
    
        self.points = points
        self.interval = interval
        self.start = points[0][0]
        self.finish = points[-1][0]
        
        self.series = self.__split_series()
        
    
    
    def __split_series(self):
        offset = self.points[0][0]
        maxval = (self.points[-1][0] - offset) // self.interval
        vals = defaultdict(list)
        for key, value in self.points:
            vals[(key - offset) // self.interval].append(value)
        series = [vals[i] for i in xrange(maxval + 1)]
        return series
        
    """
    def __split_series(self):
        end_of_chunk = self.interval
        chunk = []
        for marker, item in self.points:
            if marker > end_of_chunk:
                for end_of_chunk in xrange(end_of_chunk, marker, self.interval):
                    yield chunk
                    chunk = []
                end_of_chunk += self.interval
            chunk.append(item)
        yield chunk
        
    """   
        


import time



t = time.clock()    
a = 0
b = 1000000
points = []
for x in range(2000000):
    points.append((a, b))
    a += 1
    b += 1
print time.clock() - t



"""
points = [
    (3, 'a'), 
    (3, 'b'), 
    (3, 'a'), 
    (3, 'd'), 
    (4, 'c'),
    (16, 'e'),
    (36, 'a'),
]


points = [(1, 'a'), (2, 'b'), (2, 'a'), (3, 'd'), (8, 'c')]
"""

t = time.clock()
series = Series(points, 10000)
series = list(series.series)
print time.clock() - t

#print list(series.series)


    
    
    