# coding: utf-8


class Filter(object):
    """消息过滤器基类"""

    def filter(self, msg):
        raise NotImplemented
