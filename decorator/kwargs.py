def logger(func):
    def inner(*args, **kwargs): #1
        print "Arguments were: %s, %s" % (args, kwargs)
        return func(*args, **kwargs) #2
    return inner


@logger
def foo1(x, y=1):
    return x * y


foo1(5, 4)

foo1(7, y=8)

foo1(x=7, y=8)