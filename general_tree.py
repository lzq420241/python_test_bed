class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

def post_order(Node, children):
    if not children:
        return
    for c in children:
        post_order(c, c.children)
        print(c.data)

n = Node(1)
p = Node(1.1)
q = Node(1.2)
q1 = Node(1.21)
q2 = Node(1.22)
q21 = Node(1.221)
q22 = Node(1.222)
q2.add_child(q21)
q2.add_child(q22)

q3 = Node(1.22)
q.add_child(q1)
q.add_child(q2)
q.add_child(q3)

p1 = Node(1.11)
p2 = Node(1.12)
p.add_child(p1)
p.add_child(p2)
n.add_child(p)
n.add_child(q)

post_order(n, n.children)

