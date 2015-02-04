
class Backreader(object):
    def __init__(self,f_obj):
        self.file = f_obj
        self.gen =  iter(reversed(f_obj.readlines()))

    def readline(self):
        return next(self.gen).rsplit('\n')[0]

def reverse_readline(object):
    return iter(reversed(f_obj.readlines())).next()

f_obj = open("./lines.txt")
print type(f_obj)
br = Backreader(f_obj)
# print reverse_readline(f_obj)
for j in range(10):
    i = br.readline()
    print j,i

