__author__ = 'liziqiang'


def fuck(fn):
    print "fuck %s!" % fn.__name__[::-1].upper()


@fuck
def wfg():
    pass