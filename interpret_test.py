import sys
from cStringIO import StringIO
from code import InteractiveConsole
from contextlib import contextmanager

@contextmanager
def std_redirector(stdin=sys.stdin, stdout=sys.stdin, stderr=sys.stderr):
    tmp_fds = stdin, stdout, stderr
    orig_fds = sys.stdin, sys.stdout, sys.stderr
    sys.stdin, sys.stdout, sys.stderr = tmp_fds
    yield
    sys.stdin, sys.stdout, sys.stderr = orig_fds

class Interpreter(InteractiveConsole):
    def __init__(self, locals=None):
        InteractiveConsole.__init__(self, locals=locals)
        self.output = StringIO()

    def push(self, command):
        self.output.reset()
        with std_redirector(stdout=self.output, stderr=self.output):
            try:
                more = InteractiveConsole.push(self, command)
                result = self.output.getvalue()
            except (SyntaxError, OverflowError):
                pass
            return more, result

if __name__ == '__main__':
    import __main__
    ns = __main__.__dict__
    py = Interpreter(ns)
    py.push('a=1')
    py.push('a+=1')
    m, r = py.push('print(a+3)')
    print(r)
