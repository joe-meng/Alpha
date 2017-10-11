# coding: utf-8

from workers.share.filter import Filter


class AlertFilter(Filter):

    def filter(self, msg):
        return msg.is_alert
