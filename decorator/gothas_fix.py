__author__ = 'liziqiang'


def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to


my_list = append_to(12)
print my_list
my_other_list = append_to(42)
print my_other_list

'''
def create_multipliers():
    return [lambda x, i=i: i * x for i in range(5)]
'''

from functools import partial
from operator import mul


def create_multipliers():
    return [partial(mul, i) for i in range(5)]


for multiplier in create_multipliers():
    # 0 2 4 6 8
    print multiplier(2),