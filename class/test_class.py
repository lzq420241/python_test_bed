# Sample code from Learning Python 5th edition
class SuperMeta(type):
    def __call__(meta, classname, supers, classdict):
        print('In SuperMeta.call: ', meta, classname,
              supers, sep='\n...')
        return type.__call__(meta, classname, supers, classdict)

    def  __new__(meta, classname, supers, classdict):
        print('In SuperMeta new:', meta, classname,
              supers, sep='\n...')
        return type.__new__(meta, classname, supers, classdict)

    def __init__(Class, classname, supers, classdict):
        print('In SuperMeta.init: ', Class, classname,
              supers, sep='\n...')
        print('...init class object:', list(Class.__dict__.keys()))

print('making metaclass')


class SubMeta(type, metaclass=SuperMeta):

    def __new__(meta, classname, supers, classdict):
        print('In SubMeta.new: ', meta, classname,
              supers, sep='\n...')
        return type.__new__(meta, classname, supers, classdict)


    def __init__(Class, classname, supers, classdict):
        print('In SubMeta.init: ', Class, classname,
              supers, sep='\n...')
        print('...init class object:', list(Class.__dict__.keys()))

print('making class through type')
Eggs = type(SubMeta).__call__(SubMeta,'Eggs', (type,), {})

print('making class')
class Eggs(type, metaclass=SubMeta):
    pass
