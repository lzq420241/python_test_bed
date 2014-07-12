def decoratorFunctionWithArguments(arg1, arg2, arg3):
    """Python will take the returned function and call it at decoration time, passing the function to be decorated.
    That's why we have three levels of functions; the inner one is the actual replacement function."""
    def wrap(f):
        print "Inside wrap()"
        print "f name is %s"% f.__name__
        def wrapped_f(*args):
            print "Inside wrapped_f()"
            print "Decorator arguments:", arg1, arg2, arg3
            f(*args)
            print "After f(*args)"
        return wrapped_f
    return wrap

@decoratorFunctionWithArguments("hello", "world", 42)
def sayHello(a1, a2, a3, a4):
    print 'sayHello arguments:', a1, a2, a3, a4

print "After decoration"

print "Preparing to call sayHello()"
sayHello("say", "hello", "argument", "list")
print "after first sayHello() call"
sayHello("a", "different", "set of", "arguments")
print "after second sayHello() call"