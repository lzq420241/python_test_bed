class Singleton2(type):

    def __init__(cls, name, bases, dict):
        super(Singleton2, cls).__init__(name, bases, dict)
        print("consulting for how to init...")
        cls._instance = None

    def __call__(cls, *args, **kw):
        print("consulting for how to call...")
        if cls._instance is None:
            cls._instance = super(Singleton2, cls).__call__(*args, **kw)
        
        return cls._instance


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        print("consulting for how to call...")
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class common_handlers(metaclass=Singleton2):
    def __init__(self):
        print("run the class init...")
        self.p1 =  True
    def test(self):
        print(self.p1)
    def __getattr__(self, name):
        print("consulting for how to get attribute...")
        return False



c1 = common_handlers()
c2 = common_handlers()
print(c2.p3)

print(c1.p3)
#print(c1, c2)

#print(type(c1),type(common_handlers))

