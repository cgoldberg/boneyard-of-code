#!/usr/bin/env python
#   Corey Goldberg - 2011
#
#  - replacements for switch/case control flow
#  - call a function based on string case


def foo():
    return 'foo'
    
def bar():
    return 'bar'

def baz():
    return 'baz'


switchdict = {
    'a': foo,
    'b': bar,
    'c': baz,
}

def switch(x):
    return {
        'a': foo,
        'b': bar,
        'c': baz,
    }[x]()


if __name__ == '__main__':
    print switchdict['a']()
    print switch('b')
    

    