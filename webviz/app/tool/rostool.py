# -*- coding:utf-8 -*-
# 工具方法

import os
import re

def ros_master_online():
    """
    测试ros master是否在线
    """
    ret = os.popen('rosnode list')
    if 'ERROR' in ret:
        return False
    
    return True