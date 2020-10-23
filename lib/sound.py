#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ctypes


def execute(cmd):
    """
    直接执行MCI命令
    :param cmd: str 自定命令
    """
    code = ctypes.windll.winmm.mciSendStringA(cmd.encode("gbk"), None, 0, None)
    if code != 0:
        raise MCIError(code)


class MCIError(Exception):
    """MCI异常"""
    def __init__(self, code):
        super().__init__()
        self.msg = "[MCI Error %d] %d" % (code, code)

    def __str__(self):
        return self.msg


class Mp3:
    def __init__(self, filename, alias="music"):
        """
        :param filename: str 文件路径
        :param alias: str 文件名别名, 可以忽略
        """
        self.alias = alias
        execute("open \"%s\" alias %s" % (filename, self.alias))

    def reload(self, filename):
        """重新加载新的文件"""
        execute("open \"%s\" alias %s" % (filename, self.alias))

    def play(self):
        """从头播放"""
        execute("play %s from 0" % self.alias)

    def pause(self):
        """暂停"""
        execute("pause %s" % self.alias)

    def resume(self):
        """继续播放"""
        execute("resume %s" % self.alias)

    def stop(self):
        """停止播放"""
        execute("stop %s" % self.alias)

    def jumpto(self, time):
        """
        将播放跳转到指定时间
        :param time: int 跳转毫秒数
        """
        execute("stop %s" % self.alias)
        execute("play %s from %d" % (self.alias, time))

    def set_volume(self, volume: int):
        """
        调节音量
        :param volume: int 音量大小
        """
        execute("setaudio %s volume to %d" % (self.alias, volume))

    def close(self):
        """释放文件, 关闭播放"""
        execute("close %s" % self.alias)


class Record:
    def __init__(self, save_file, alias="wave"):
        self.save_file = save_file
        self.alias = alias
        execute("open new type WAVEAudio alias %s" % alias)

    def set_attribute(self, f_parm, p_parm):
        return execute("set %s %s %s" % (self.alias, f_parm, p_parm))

    def start(self):
        execute("record %s" % self.alias)

    def finish(self):
        execute("stop %s" % self.alias)

    def save(self):
        execute("save %s" % self.alias)

    def close(self):
        execute("close %s" % self.alias)
