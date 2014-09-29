from time import ctime

"""
Because the function wrapper_func references the func variable,
it is kept alive after the test_func function has returned.

So, if your nested functions don't:
1.access variables that are local to enclosing scopes
2.do so when they are executed outside of that scope

they will not be a closure.

with just read-only closure you can at least implement
the function decorator pattern for which Python offers syntactic sugar.

"""


def test_func(func):
    def wrapper_func():
        print "[%s] %s() called" % (ctime(), func.__name__)
        return func()

    return wrapper_func


@test_func
def f1():
    print "call f1"


@test_func
def f2():
    print "call f2"


@test_func
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