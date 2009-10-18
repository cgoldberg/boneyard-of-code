#!/usr/bin/env python
# Corey Goldberg


from collections import defaultdict



class Series(object):

    def __init__(self, points, interval):
        # points is a list of tuples: (sec, value)
        # interval is in secs
    
        self.points = points
        self.interval = interval
        self.start = points[0][0]
        self.finish = points[-1][0]
        self.algo = 'lazy'
        
        self.series = self.__split_series()
        
    
    def __split_series(self):
        if self.algo == 'dict':
            return self.__split_series_dict()
        elif self.algo == 'lazy':
            return self.__split_series_lazy()
        else:
            raise Exception('unknown algorithm')
            
        
    def __split_series_dict(self):
        offset = self.points[0][0]
        maxval = (self.points[-1][0] - offset) // self.interval
        vals = defaultdict(list)
        for key, value in self.points:
            vals[(key - offset) // self.interval].append(value)
        series = [vals[i] for i in xrange(maxval + 1)]
        return series
        

    def __split_series_lazy(self):
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
        
       
        





points = [(1, 'a'), (2, 'b'), (2, 'a'), (3, 'd'), (8, 'c')]
s = Series(points, 3)
print list(s.series)

    
    
    