# -*- coding:utf-8 -*-
from app.core import context
from app.views import client_list


class Control:

    def __init__(self):
        pass

    def excute(self, c):
        client_list.show_client_msg(c.data)