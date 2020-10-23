#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os.path import split, getsize
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from sys import argv
from time import sleep

PATH = split(argv[0])[0]
DL_PATH = "%s/dl" % PATH


def send_file(file_name, conn: socket):
    file = open(file_name, "rb")  # 文件对象
    length = getsize(file_name)  # 文件大小
    data = bytes
    try:
        print(("%s\n%d" % (split(file_name)[1], length)).encode())
        conn.send(("%s\n%d" % (split(file_name)[1], length)).encode())
        if conn.recv(3) != b"suc":
            return False
        while data != b"":
            data = file.read(65536)
            conn.send(data)
    except Exception as err:
        print(err)
        return False
    else:
        return True
    finally:
        file.close()


def recv_file(conn: socket, path=DL_PATH):
    try:
        data_size = 0
        args = conn.recv(1024).decode()
        file_name = args.split("\n")[0]
        file_size = int(args.split("\n")[1])
        file = open("%s/%s" % (path, file_name), "wb")
        conn.send(b"suc")

        while True:
            data = conn.recv(65536)
            file.write(data)
            data_size += len(data)
            if data_size >= file_size:
                break
        file.close()
    except Exception:
        return False
    else:
        return True


def send_data(conn: socket, data: bytes):
    data_len = len(data)
    conn.send(b"%d" % data_len)
    if conn.recv(10) != b"%d" % data_len:
        raise Exception("Send data failure")
    conn.send(data)


def recv_data(conn: socket):
    buff = b""
    data_len = int(conn.recv(10).decode())
    conn.send(b"%d" % data_len)
    while len(buff) < data_len:
        buff += conn.recv(1024)
    return buff


def get_host_ip():
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def broadcast():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    while True:
        try:
            sock.sendto(b"00296966A71EBEAC", ("<broadcast>", 60720))
        except Exception:
            return
        sleep(2)
