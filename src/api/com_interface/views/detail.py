#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-06-13

@author: Devin
"""
import logging
import json


import requests

from common.models import BackstageHTTPResponse, PageInfo, APIEncoder
from common.views import BackstageBaseAPIView
from common.utils import gen_like_filter_mongo
from common.utils import gen_page_info_mongo
from common.utils import get_mongo_id
from common.utils import log_exception
from com_interface.lib import MapInterfaceObject
from django.conf import settings
LOCAL_URL  = settings.LOCAL_URL


logger = logging.getLogger("use_info_ms")


class DetailView(BackstageBaseAPIView, MapInterfaceObject):

    @log_exception
    def get(self, request, pk):
        u"""
        根据ID获取新闻
        ---

        parameters:
            - name: pk
              description: news id
              type: string
              paramType: path
              required: true
            - name: type_id
              description: 分类id,只能传一个
              type: string
              paramType: query
              required: true
        """
        type_name_vals = {'2': 'zixun', '3': 'zhibo', }
        query_dict = request.query_params.dict().copy()
        new_query_dict = self.get_mapping_query(query_dict)
        type_id = query_dict.get('type_id', '')
        # is_recommend = query_dict.get('is_recommend')
        # order = query_dict.get('order')
        # order_by = query_dict.get('order_by')
        # if order == 'desc':
        #     if order_by == 'click_count':
        #         new_query_dict['desc'] = 'click_count'
        #     elif order_by == 'inputtime':
        #         new_query_dict['desc'] = 'pub_time'
        #
        # if str(is_recommend) == '1':
        #     new_query_dict['top_tag'] = '1'
        res = self.init_res()
        if type_id == '1':
            return self.get_http_res(res)
        elif type_id == '2':
            r = requests.get(LOCAL_URL+'news/news/%s'%str(pk))
            content = json.loads(r.content)
        elif type_id == '3':
            r = requests.get(LOCAL_URL+'news/live/%s'%str(pk))
            content = json.loads(r.content)
        else:
            return self.get_http_res(res)
        vals = self.get_res_list_data([content['data']], type_id, type_name_vals.get(type_id))
        data = vals and vals[0]
        data['more_data'] = {
                "id": data['id'],
                "news_id": data['id'],
                "content": content['data'].get('content_html'),
            }
        # meta = self.get_res_meta(content['pageinfo'])
        res = self.init_res(data)
        return self.get_http_res(res)
