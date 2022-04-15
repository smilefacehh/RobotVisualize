# -*- coding:utf-8 -*-
# 工具方法

import os
import re
import uuid
import socket 
from app.tool import util

def host_ip():
    """
    本机ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

def host_mac():
    """
    本机mac地址
    """
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])


def lan_devices():
    """
    局域网设备ip、mac列表
    """
    devices = {}

    my_ip = host_ip()
    my_mac = host_mac()
    devices[my_ip] = my_mac

    try:
        ret = os.popen('arp -a').read()
        lines = ret.split('\n')
        for line in lines:
            match_obj = re.match(r'.*\((\d+\.\d+\.\d+\.\d+)\).*([0-9a-zA-Z]{2}:[0-9a-zA-Z]{2}:[0-9a-zA-Z]{2}:[0-9a-zA-Z]{2}:[0-9a-zA-Z]{2}:[0-9a-zA-Z]{2}).*', line)
            if match_obj:
                devices[match_obj.group(1)] = match_obj.group(2)
    except Exception as e:
        print(e)

    devices = sorted(devices.items(), key=lambda x:x[0], reverse=False)
    return devices


def valid_ip(ip):
    """
    判断是否有效ip
    """
    ip_arr = ip.split('.')
    if len(ip_arr) != 4:
        return False
    
    for num in ip_arr:
        n = util.str2int(num)
        if n is None:
            return False
        if n < 0 or n > 255:
            return False

    return True