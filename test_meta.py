class Meta(type):
    """
    no bases and no explicit metaclass are given, then type() is used
    """
    pass

class MyClass(metaclass=Meta):
    """
    an explicit metaclass is given and it is not an instance of type(), 
    then it is used directly as the metaclass
    """
    pass

class MySubclass(MyClass):
    pass

class commonClass(object):
    """
    no bases and no explicit metaclass are given, then type() is used
    """
    pass

print(Meta.__class__)
print(MyClass.__class__)
print(type(MySubclass))
print(isinstance(MySubclass, type(MySubclass)))
print(MySubclass.__class__)
print(commonClass.__class__)