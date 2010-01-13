#!/usr/bin/env python
#
# ascii command-line progress bar with percentage and elapsed time display
#
# modified by Corey Goldberg - 2010
# adapted from Pylot source code,  original by Vasil Vangelovski



class ProgressBar:
    def __init__(self, duration, min_value=0, max_value=100, total_width=50):
        self.prog_bar = '[]'
        self.duration = duration
        self.min = min_value
        self.max = max_value
        self.span = max_value - min_value
        self.width = total_width
        self.amount = 0 
        self.__update_amount(0)
    
    def __update_amount(self, new_amount=0):
        if new_amount < self.min: new_amount = self.min
        if new_amount > self.max: new_amount = self.max
        self.amount = new_amount
        diff_from_min = float(self.amount - self.min)
        percent_done = int(round((diff_from_min / float(self.span)) * 100.0))
        all_full = self.width - 2
        num_hashes = int(round((percent_done / 100.0) * all_full))
        self.prog_bar = '[' + '#' * num_hashes + ' ' * (all_full - num_hashes) + ']'
        pct_place = (len(self.prog_bar) / 2) - len(str(percent_done))
        pct_string = '%i%%' % percent_done
        self.prog_bar = self.prog_bar[0:pct_place] + (pct_string + self.prog_bar[pct_place + len(pct_string):])
        
    def update_time(self, elapsed_secs):
        self.__update_amount((elapsed_secs / float(self.duration)) * 100)
        self.prog_bar += '  %ds/%ss' % (elapsed_secs, self.duration)
        
    def __str__(self):
        return str(self.prog_bar)
        
        
        
if __name__ == '__main__':
    p = ProgressBar(60)
    p.update_time(20)
    print p