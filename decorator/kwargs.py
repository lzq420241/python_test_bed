"""
args are tuple, kwargs are dict.
"""


def logger(func):
    def inner(*args, **kwargs):
        print "Arguments were: %s, %s" % (args, kwargs)
        return func(*args, **kwargs)
    return inner


@logger
def foo1(x, y=1):
    return x * y


print foo1(5)

print foo1(5, 4)

foo1(7, y=8)

print foo1(x=7, y=8)