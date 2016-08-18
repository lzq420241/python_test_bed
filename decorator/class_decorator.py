class myDecorator(object):
 
    def __init__(self, fn):
        print("inside myDecorator.__init__()")
        self.fn = fn
 
    def __call__(self, *args):
        self.fn(*args)
        print("inside myDecorator.__call__()")

class C(object):
    def __init__(self, r):
        self.r = r
    @myDecorator
    def aFunction(self, a):
        self.r = a
        print("inside aFunction()")
 
print("Finished decorating aFunction()")
 
# c = C('r')
C.aFunction('a')