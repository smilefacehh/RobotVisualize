# -*- coding:utf-8 -*-
# 展示元素

from sys import stderr


color = ['brown', 'blue', 'red', 'green', 'black', 'tomato', 'gray', 'indigo', 'yellow', 'gold']

class ShowItem:
    """展示条目
    
    一个ShowItem对应一个展示字段。

    Attributes:
        topic_uri: Topic名称
        msg_type: 消息类型，例如：Protocol.ImuWithOdometryMSG
        attr: 展示的属性字段，例如：imu.roll
        show_label: 展示标签名称
    """

    def __init__(self, topic_uri, msg_type, attr, show_label) -> None:
        self.topic_uri = topic_uri
        self.msg_type = msg_type
        self.attr = attr
        self.show_label = show_label

    def print(self):
        print("{},{},{},{}".format(self.topic_uri,self.msg_type,self.attr,self.show_label), file=stderr)


class ShowBlock:
    """展示块

    多个ShowItem放在一起展示，构成ShowBlock。
    
    Attributes:
        block_title: 标题
        show_items: ShowItem列表
    """

    def __init__(self, block_title) -> None:
        self.block_title = block_title
        self.show_items = list()

    def print(self):
        print(self.block_title, file=stderr)
        for item in self.show_items:
            item.print()


class ShowFigure:
    """展示图像
    
    多个ShowBlock放在一起，构成一幅图像
    
    Attributes:
        figure_title: 标题
        show_blocks: ShowBlock列表
    """

    def __init__(self, figure_title) -> None:
        self.figure_title = figure_title
        self.show_blocks = list()

    def print(self):
        for block in self.show_blocks:
            block.print()
