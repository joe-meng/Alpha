# -*- coding: utf-8 -*-
from mongoengine import *


connect('jeff')


class BackstageNewsModels(Document):
    """新闻消息对象"""

    title = StringField()
    url = StringField()
    abstract = StringField()
    content_html = StringField()
    website = StringField()
    view = StringField()
    author = StringField()
    pub_time = StringField()
    craw_time = StringField()
    category = StringField()
    actor = StringField()
    daodu = StringField()
    content_text = StringField()
    machine_class = StringField()



def test():
    x = BackstageNewsModels(title='test1', actor='12345')
    x.save()

if __name__ == '__main__':
    test()