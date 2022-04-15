# -*- coding:utf-8 -*-
# 工具方法

import os
import re

def adb_connected(ip):
    """
    设备是否通过adb连接上了
    @ret: bool 是否连接上
    """
    ret = os.popen('adb devices').read()
    return True if ip in ret else False


def adb_connect(ip):
    """
    通过adb连接设备
    @ret: bool 是否连接成功
    """
    ret = os.popen('adb connect %s' % ip)
    if 'already connected to' in ret:
        os.popen('adb shell')
    else:
        return False
    return True


def adb_pull(from_path, to_path):
    """
    通过adb拉取文件
    @ret: bool 是否拉取成功 
    """
    ret = os.popen('adb devices').read()
    match_obj = re.match(r'.*\d+\.\d+\.\d+\.\d+:\d+.*', ret)
    if not match_obj:
        return False

    ret = os.popen('adb pull %s %s' % (from_path, to_path))
    if 'error' in ret:
        return False

    return True

