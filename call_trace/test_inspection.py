__author__ = 'liziqiang'

import inspect

def f1(a,b):
    print a+b
    cf = inspect.currentframe()
    print inspect.getargvalues(cf)
    while cf.f_back.f_back:
        cf = cf.f_back
        print cf.f_locals
        arg = inspect.getargvalues(cf)
        print inspect.formatargvalues(arg)

def f2(c,d):
    f1(c,d)


f2(3,4)
