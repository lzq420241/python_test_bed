__author__ = 'liziqiang'


def append_to(element, to=[]):
    to.append(element)
    return to


my_list = append_to(12)
my_other_list = append_to(42)
"""
Python's default arguments are evaluated once when the function is defined,
not each time the function is called.
[12, 42]
"""
print my_other_list


def create_multipliers():
    return [lambda x: i * x for i in range(5)]


for multiplier in create_multipliers():
    """
    Python's closures are late binding.
    This means that the values of variables used in closures are looked up
    at the time the inner function is called.
    8 8 8 8 8
    """
    print multiplier(2),