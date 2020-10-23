#!/usr/bin/env python
# -*- coding:utf-8 -*-

from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM, timeout
from time import sleep

host_list = []
s = socket(AF_INET, SOCK_DGRAM)
s.bind(("", 60720))
s.settimeout(1)


class MyThread(Thread):
    def __init__(self, func):
        super().__init__()
        self.alive = True
        self.func = func

    def run(self):
        while True:
            if not self.alive:
                break
            self.func()

    def stop(self):
        self.alive = False


def search():
    try:
        data, addr = s.recvfrom(50)
    except timeout:
        return
    if data == b"00296966A71EBEAC":
        if addr[0] not in host_list:
            host_list.append(addr[0])


def main():
    thread = MyThread(search)
    thread.setDaemon(True)
    thread.start()
    sleep(10)
    thread.stop()
    print("Host:\n%s" % "\n".join(host_list))


if __name__ == '__main__':
    main()
