#!/usr/bin/python
import sys
from cStringIO import StringIO
from code import InteractiveConsole
from contextlib import contextmanager

import socket
import sys, time, select

class MySocket(socket.socket):
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, _sock=None):
        socket.socket.__init__(self, family, type, proto, _sock)
        
    def write(self, text):
        return self.send(text)
    
    def readlines(self):
        return self.recv(2048)
    
    def read(self):
        return self.recv(1024)
    
    def accept(self):
        conn, addr = socket.socket.accept(self)
        return MySocket(_sock=conn), addr 


@contextmanager
def std_redirector(stdin=sys.stdin, stdout=sys.stdin, stderr=sys.stderr):
    tmp_fds = stdin, stdout, stderr
    orig_fds = sys.stdin, sys.stdout, sys.stderr
    sys.stdin, sys.stdout, sys.stderr = tmp_fds
    yield
    sys.stdin, sys.stdout, sys.stderr = orig_fds

class Interpreter(InteractiveConsole):
    def __init__(self, locals=None, fd=None):
        InteractiveConsole.__init__(self, locals=locals)
        self.fd = fd

    def push(self, command):
        with std_redirector(stdin=self.fd, stdout=self.fd, stderr=self.fd):
            InteractiveConsole.push(self, command)

if __name__ == '__main__':
    import __main__
    ns = __main__.__dict__
    try:
        serversocket = MySocket()
        serversocket.bind(("", 12345))
        serversocket.listen(1)
        conn, addr = serversocket.accept()
        py = Interpreter(ns,conn)
        py.push('a=1')
        py.push('a+=1')
        sys.stdin = conn
        # print(sys.stdin.read())
        while select.select([conn], [], []):
            time.sleep(1)
            py.push(sys.stdin.read())
    except:
        import traceback
        traceback.print_exc()
