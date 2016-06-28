
class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value

@memoized
class Node(object):
    # __metaclass__ = Singleton
    def __init__(self, data_s, data_c, data_e):
        self.data_s = data_s
        self.data_c = data_c
        self.data_e = data_e
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

def post_order(Node, children):
    print(Node.data_s)
    if not children:
        print(Node.data_c)
        return
    for c in children:
        post_order(c, c.children)
        print(c.data_e)

n = Node('1s','','1e')
p = Node('1.1s','','1.1e')
pn = Node('1.1s','','1.1e')
assert p==pn
q = Node('1.2s','','1.2e')
q1 = Node('1.21s','','1.21e')
q2 = Node('1.22s','','1.22e')
q21 = Node('1.221s','1.221c','1.221e')
q22 = Node('1.222s','','1.222e')
q2.add_child(q21)
q2.add_child(q22)

q3 = Node('1.23s','1.23c','1.23e')
q.add_child(q1)
q.add_child(q2)
q.add_child(q3)

p1 = Node('1.11s','','1.11e')
p2 = Node('1.12s','','1.12e')
p.add_child(p1)
p.add_child(p2)
n.add_child(p)
n.add_child(q)

post_order(n, n.children)

