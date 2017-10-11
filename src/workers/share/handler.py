# coding: utf-8
import logging

from .viewer import Message


class Handler(object):
    viewers = []
    filters = []
    msg_class = Message

    def set_msg_class(self, msg_class):
        self.msg_class = msg_class

    def do_handle(self, text):
        msg = self.msg_class(text)
        if self.filter(msg):
            self.notify(msg)

    def add_viewer(self, viewer):
        if viewer not in self.viewers:
            self.viewers.append(viewer)

    def remove_viewer(self, viewer):
        if viewer in self.viewers:
            self.viewers.remove(viewer)

    def add_filter(self, filter):
        if not (filter in self.filters):
            self.filters.append(filter)

    def remove_filter(self, filter):
        if filter in self.filters:
            self.filters.remove(filter)

    def notify(self, msg):
        for viewer in self.viewers:
            try:
                viewer.update(msg)
            except Exception as e:
                logging.error(str(e))

    def filter(self, msg):
        rv = True
        for f in self.filters:
            if hasattr(f, 'filter'):
                result = f.filter(msg)
            else:
                result = f(msg)
            if not result:
                rv = False
                break
        return rv
