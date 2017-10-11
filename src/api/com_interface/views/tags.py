#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-06-13

@author: Devin
"""
import logging

from common.views import BackstageBaseAPIView
from common.utils import log_exception
from com_interface.lib import MapInterfaceObject

logger = logging.getLogger("use_info_ms")


class TagView(BackstageBaseAPIView, MapInterfaceObject):

    @log_exception
    def get(self, request):
        u"""
        获取所有标签
        ---

        :param request:
        :return:
        """
        col = self.db.tag_ware
        tags = col.find()
        data = []
        for tag in tags:
            news_keys = {}
            news_keys['id'] = str(tag['_id'])
            news_keys['tag'] = tag.get('name')
            news_keys['tag_en'] = tag.get('tag')
            data.append(news_keys)
        # vals = col.find_one()
        # data = []
        # for tag in vals['tag']:
        #     news_keys = {}
        #     news_keys['id'] = str(vals['_id'])
        #     news_keys['tag'] = tag
        #     news_keys['tag_en'] = tag
        #     data.append(news_keys)
        logger.info('获取所有标签')
        res = self.init_res(data=data)
        return self.get_http_res(res)
