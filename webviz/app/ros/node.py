# -*- coding:utf-8 -*-
import sys
import rospy
from importlib import import_module
from app.ros.msg import Msg

topic_base = "protocol"

class Node:
    """节点
    
    订阅/取消订阅消息
    """

    def __init__(self, node_name) -> None:
        rospy.init_node(node_name, anonymous=False, disable_signals=True)
        self.topic_msg = dict()
        self.subscriber_list = list()
        sys.path.append("/home/lutao/narwal/pita2_workspace/devel/lib/python3/dist-packages/")


    def subscribe(self, topic_uri, msg_type):
        msg = Msg(topic_uri, msg_type)
        self.topic_msg[topic_uri] = msg
        msg_type_comp = getattr(import_module('%s.msg' % topic_base), msg_type)
        sub = rospy.Subscriber(topic_uri, msg_type_comp, self.topic_msg[topic_uri].callback)
        self.subscriber_list.append(sub)


    def spin(self):
        rospy.spin()


    def get_msg(self, topic_uri):
        if topic_uri in self.topic_msg:
            return self.topic_msg[topic_uri]
        return None