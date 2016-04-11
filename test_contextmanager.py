from contextlib import contextmanager

@contextmanager
def test(a):
    print("Entering...")
    print("the argument is %s" % a)
    # yield
    # print("Cleaning up...")
    try:
        yield
    finally:
        print("Cleaning up...")


with test(10) as f:
    raise ArithmeticError('error.')