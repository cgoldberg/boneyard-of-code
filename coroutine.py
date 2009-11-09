#!/usr/bin/env python
# Corey Goldberg - 2009
# microthreading/coroutine example using generators


from collections import deque


def main():
    task_q = deque()
    task_q.append(foo())
    task_q.append(bar())

    while task_q:
        task = task_q.pop()
        try:
            next(task)
            task_q.appendleft(task)
        except StopIteration:
            pass


def foo():
    for i in xrange(99):
        print 'hello from foo %i' % i
        yield
    
def bar():
    for i in xrange(99):
        print 'hello from bar %i' % i
        yield
        

if __name__ == '__main__':
    main()
    