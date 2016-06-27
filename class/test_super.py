from collections import Counter, OrderedDict

class OrderedCounter(Counter, OrderedDict):
     'Counter that remembers the order elements are first seen'
     def __repr__(self):
         return '%s(%r)' % (self.__class__.__name__,
                            OrderedDict(self))
     # def __reduce__(self):
     #     return self.__class__, (OrderedDict(self),)

oc = OrderedCounter('abracadabra')
print(oc)

class Person:
    def __init__(self, name):
        self.name = name
    
    # Getter function
    @property
    def name(self): 
        return self._name

    # Setter function
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string') 
            self._name = value

    # Deleter function
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")


class SubPerson(Person): 
    @property
    def name(self): 
        print('Getting name') 
        return super().name
        
    @name.setter
    def name(self, value):
        print('Setting name to', value)
        """
        super([type[, object-or-type]])
        If the second argument is a type, issubclass(type2, type) must be true.
        This is useful for classmethods.
        The use of double leading underscores causes the name to be mangled to something else,
        so that such attributes cannot be overridden via inheritance.

        """
        super(SubPerson, SubPerson).name.__set__(self, value)
        
    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)

s = SubPerson('Guido')
s.name = 'Larry'
s.name = 42
