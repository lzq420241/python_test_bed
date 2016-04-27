class RevealAccess(object):
    """
    A data descriptor that sets and returns values
    normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, cls):
        """
        obj will be set to None, if RevealAccess is used inside class.
        cls will be set to MyClass for this example
        """
        print('Retrieving %s' % self.name)
        return self.val

    def __set__(self, obj, val):
        print('Updating %s' % self.name)
        self.val = val


class MyClass(object):
    """
    A more idiomatic way will be like this:
    _x = 0
    @property
    def x(self):
        return type(self)._x
    """
    x = RevealAccess(10, 'var "x"')
    y = 5


m = MyClass()
print(m.x)
m.x = 20