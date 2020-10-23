#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os import mkdir
from os.path import exists
from re import match
from socket import socket, timeout
from sys import argv

from lib.network import send_file, recv_file, recv_data
from lib.search import main as search_host

args = argv[1:]  # 获得命令行参数

# 检查参数
if not args:
    print("""Usage: 
    python conn.py [Address] [Port]
    python conn.py -s""")
    exit()
elif args[0] == "search" or args[0] == "-s":
    search_host()
    exit()

# 创建 日志下载 文件夹
if not exists("./log"):
    mkdir("./log")

address = args[0]
port = int(args[1] if len(args) > 1 else 60724)  # 默认端口724
conn = socket()


def _main():
    try:
        conn.connect((address, port))
    except (timeout, OSError):
        print("Connect Failure. Maybe there are some problems with the server.")
        conn.close()
        return

    # 检查指令并发送
    while True:
        cmd = input(" > ")

        if not cmd:
            continue
        elif cmd == "exit":
            conn.send(b"exit")
            break
        elif match("sendfile ", cmd):
            filename = cmd.split()[1]
            if not exists(filename):
                print("No such file")
            else:
                conn.send(b"sendfile")
                send_file(filename, conn)
        elif match("getfile", cmd):
            conn.send(cmd.encode())
            status = recv_data(conn)
            if status != b"0":
                print(status.decode())
            else:
                recv_file(conn)
            continue
        elif match("log ", cmd):
            conn.send(cmd.encode())
            if cmd.split()[1] == "get":
                recv_file(conn, path="./log")
        else:
            conn.send(cmd.encode())

        result = recv_data(conn).decode()
        print(result)


def main():
    global conn
    try:
        _main()
    except ConnectionResetError:
        print("Connect Error. Try to connect again......")
        conn.close()
        # 尝试重连
        try:
            conn = socket()
            main()
        except Exception as err:
            print(err)
            print("Connect Failure. Please check your network.")
            return


if __name__ == '__main__':
    main()
