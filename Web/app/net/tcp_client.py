# -*- coding:utf-8 -*-
# tcp client

import socket
import fcntl, errno
import threading
import os, sys
from app.core import context, control


# 尝试连接次数
RETRY_TIMES = 5
RECV_BUFFER_SIZE = 1024

class TcpClient:

    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fcntl.fcntl(self.client, fcntl.F_SETFL, os.O_NONBLOCK)

        try_time = 0
        while True:
            try:
                self.client.connect((ip, port))
                print("Connect server %s:%s succeed." % (ip, port))
                break
            except socket.error as e:
                try_time += 1
                print("%s, retry %d" % (e, try_time))

                if try_time == RETRY_TIMES:
                    print("Reach max retry times, exit.")
                    self._ok = False
                    break
                    # os._exit(-1)

        recv_thread = threading.Thread(target=self.recv)
        recv_thread.start()
        self._ok = True
        self.control = control.Control()


    def recv(self):
        while True:
            try:
                msg = self.client.recv(RECV_BUFFER_SIZE)
                msg = msg.decode('utf-8')
                if msg != '':
                    print("Recv msg: %s" % msg)
                    if msg == 'close':
                        self.client.close()
                        print("Rejected by server, now close and exit.")
                        break
                        # os._exit(-1)
                    c = context.Context(msg)
                    self.notify(c)

            except socket.error as e:
                if e.args[0] == errno.EAGAIN or e.args[0] == errno.EWOULDBLOCK:
                    continue
                else:
                    print("%s, now close and exit." % e)
                    self.client.close()
                    self._ok = False
                    break
                    # os._exit(-1)


    def send(self, msg):
        try:
            self.client.send(msg.encode('utf-8'))
        except socket.error as e:
            print("%s, now close and exit." % e)
            self.client.close()
            # os._exit(-1)

    def notify(self, context):
        self.control.excute(context)

    def close(self):
        self.client.close()

    def ok(self):
        return self._ok



if __name__ == "__main__":
    client = TcpClient('127.0.0.1', 10002)
    while True:
        msg = input("send msg:")
        client.send(msg)