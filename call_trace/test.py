__author__ = 'liziqiang'

import inspect

def f1(a,b,c=5):

    for st in inspect.stack()[1::-1]:
        #frame
        cf = st[0]
        #file
        fp = st[1]
        #line
        ln = st[2]
        #func
        fn = st[3]

        arg_info = inspect.getargvalues(cf)
        args = arg_info.args
        locs = arg_info.locals

        arg_value = ["%s=%s" %(x,locs[x]) for x in args]

        message = 'File "%s", line %s\n%s%s' %(fp, ln, fn, tuple(arg_value))
        print message
    return a+b+c

def f2(c,d):
    f1(c,b=5)
    f1(7,3)
    #raise NameError("%s" % f1(c,b=5))


if __name__ == '__main__':
    '''x = raw_input("input a:")
    y = raw_input("input b:")
    f2(int(x), int(y))'''
    f2(6,9)
