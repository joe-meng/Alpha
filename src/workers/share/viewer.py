# coding: utf-8


class Message(object):
    """消息类供消息观察者使用"""

    def __init__(self, text):
        self.text = text


class MessageViewer(object):
    """消息观察者基类"""

    def update(self, msg):
        raise NotImplemented
