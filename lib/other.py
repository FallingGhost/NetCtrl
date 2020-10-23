#!/usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess
from os import getcwd, chdir
from re import search
from time import strftime

LOG_FILENAME = "%s.log" % strftime("%m.%d")


def popen(cmd):
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE
    )
    stdout, _ = proc.communicate()
    result = stdout.decode('gbk')
    code = proc.returncode
    return result, code


def log_write(msg, current_path):
    with open("%s/.log/%s" % (current_path, LOG_FILENAME), "a") as log:
        log.write("[%s] %s\n" % (strftime("%H:%M:%S"), msg))


def release_port():
    string = popen("netstat -ano | findstr 60724")[0]
    match = search("\d+$", string)
    if match:
        popen("taskkill /f /pid %s" % match.group())


def cd(args):
    if len(args) == 0:
        return getcwd()
    else:
        try:
            chdir(" ".join(args))
        except FileNotFoundError:
            return "No such direction"
        return " "
