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
LOCAL_URL = settings.LOCAL_URL


logger = logging.getLogger("use_info_ms")


class StalistView(BackstageBaseAPIView, MapInterfaceObject):


    @log_exception
    def get(self, request):
        u"""
        翻页获取统计列表(目前只有点击)
        ---

        parameters:
            - name: per_page
              description: 每页显示数量,default = 20
              type: string
              paramType: query
              required: false
            - name: type_id
              description: 分类id,只能传一个
              type: string
              paramType: query
              required: false
            - name: tag_en
              description: 标签的缩写,多个tag_en以英文,隔开
              type: string
              paramType: query
              required: false
            - name: page
              description: 第几页
              type: string
              paramType: query
              required: false
            - name: order_by
              description: 目前有意义的排序的只有这两个值为， click_count 按点击量排序, inputtime 按文章写入时间排序， 默认为 click_count
              type: string
              paramType: query
              required: false
            - name: order
              description: desc 倒叙, asc 顺序， 默认desc倒叙
              type: string
              paramType: query
              required: false
            - name: machine_class
              description: 资讯品目(Others,Al,Cu,Fe,PVC,Pb,Zn)
              type: string
              paramType: query
              required: false
        """

        type_name_vals = {'2': 'zixun', '3': 'zhibo', }
        query_dict = request.query_params.dict().copy()
        new_query_dict = self.get_mapping_query(query_dict)
        type_id = query_dict.get('type_id', '')
        is_recommend = query_dict.get('is_recommend')
        new_query_dict['pub_state'] = '1'
        if str(is_recommend) == '1':
            new_query_dict['top_tag'] = '1'
        # if query_dict.get('tag_en'):
        #     new_query_dict['manual_tags'] = json.dumps(query_dict.get('tag_en').split(','))

        order = query_dict.get('order')
        order_by = query_dict.get('order_by')
        if order == 'desc':
            if order_by == 'click_count':
                new_query_dict['desc'] = 'click_count'
            elif order_by == 'inputtime':
                new_query_dict['desc'] = 'pub'


        res = self.init_res()
        if type_id == '1':
            new_query_dict['is_recommand'] = '1'
            r = requests.get(LOCAL_URL + 'news/news/', params=new_query_dict)
            content = json.loads(r.content)
        elif type_id == '2':
            r = requests.get(LOCAL_URL + 'news/news/', params=new_query_dict)
            content = json.loads(r.content)
        elif type_id == '3':
            r = requests.get(LOCAL_URL + 'news/live/', params=new_query_dict)
            content = json.loads(r.content)
        elif type_id == '4':
            new_query_dict['manual_tags'] = '精选'
            r = requests.get(LOCAL_URL + 'news/news/', params=new_query_dict)
            content = json.loads(r.content)
        elif type_id == '5':
            new_query_dict['manual_tags'] = '数据'
            r = requests.get(LOCAL_URL + 'news/news/', params=new_query_dict)
            content = json.loads(r.content)
        else:
            return self.get_http_res(res)

        if not content['data']:
            content['data'] = []

        data = self.get_res_list_data(content['data'], type_id, type_name_vals.get(type_id))
        meta = self.get_res_meta(content['pageinfo'])
        res = self.init_res(data, meta)
        return self.get_http_res(res)



