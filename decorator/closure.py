from time import ctime, sleep


def testfunc(func):
    def wrapperfunc():
        print "[%s] %s() called" % (ctime(), func.__name__)
        return func()
    return wrapperfunc


@testfunc
def f1():
    print "call f1"


@testfunc
def f2():
    print "call f2"


@testfunc
def f3():
    print "call f3"


def dec(f):
    def wrapper():
        f1()
        f2()
        f3()
        return f()
    return wrapper


@dec
def f4():
    print 'call f4'

f4()
