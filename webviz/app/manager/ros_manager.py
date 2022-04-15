# -*- coding:utf-8 -*-
# ros管理

from sys import stderr
from app.ros.node import Node
from app.ros.plot_elem import ShowFigure
from app.manager.singleton import singleton

@singleton
class RosManager:
    """ros管理，单例
    
    ros流程调度，数据管理
    """

    def __init__(self) -> None:
        self.node = Node("Webviz")
        self.show_figure = None

    def subscribe(self, show_figure):
        self.show_figure = show_figure
        topic_type = dict()
        for block in show_figure.show_blocks:
            for item in block.show_items:
                if item.topic_uri not in topic_type:
                    topic_type[item.topic_uri] = item.msg_type
        
        for k,v in topic_type.items():
            self.node.subscribe(k, v)
            print("Subscribe:%s" % k, file=stderr)

    def loop_end(self):
        self.node.spin()

    
    def get_data(self):
        """获取所有数据，按block返回列表

        returns:
            [[1,2,3,4],[1,2],...]
        """
        data = []
        for block in self.show_figure.show_blocks:
            data.append([])
            for item in block.show_items:
                val = self.node.get_msg(item.topic_uri).get_attr_val(item.attr)
                data[-1].append(val)

        return data

    
    def get_figure_size(self):
        """获取每个block的item数量，返回列表

        returns:
            [4,2]
        """
        sz = []
        for block in self.show_figure.show_blocks:
            sz.append(len(block.show_items))
        return sz

    def get_block_num(self):
        """获取block数量"""
        return len(self.show_figure.show_blocks)