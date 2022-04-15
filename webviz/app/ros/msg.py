# -*- coding:utf-8 -*-

class Msg:
    """消息

    接收数据，获取字段内容

    Attributes:
        topic_uri: topic名称
        msg_type: 消息类型
        msg: 消息实体
    """

    def __init__(self, topic_uri, msg_type) -> None:
        self.topic_uri = topic_uri
        self.msg_type = msg_type
        self.msg = None

    
    def callback(self, msg):
        """消息回调"""
        self.msg = msg

    
    def get_attr_val(self, attr):
        """从msg中获取属性字段对应的值"""
        data = self.msg
        if data is None:
            return 0
        
        attr_list = attr.split('.')
        for a in attr_list:
            data = getattr(data, a)
        
        return data