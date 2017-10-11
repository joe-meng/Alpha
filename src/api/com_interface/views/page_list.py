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


class PageListView(BackstageBaseAPIView, MapInterfaceObject):


    @log_exception
    def get(self, request):
        u"""
        翻页获取资讯列表(需要显示总数以及分页的)
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
            - name: is_recommend
              description: 是否置顶,0非置顶，1置顶。 >1 或者 不传则取 全部
              type: string
              paramType: query
              required: false
            - name: page
              description: 第几页
              type: string
              paramType: query
              required: false
            - name: tag_en
              description: 标签的缩写,多个tag_en以英文,隔开
              type: string
              paramType: query
              required: false
            - name: s
              description: 搜索文字
              type: string
              paramType: query
              required: false
            - name: keyword
              description: 关键词,按英文逗号分开
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

        new_query_dict['descent'] = 'pub'
        new_query_dict['pub_state'] = '1'
        res = self.init_res()
        if type_id == '1':
            new_query_dict['is_recommand'] = '1'
            r = requests.get(LOCAL_URL + 'news/news/', params=new_query_dict)
            content = json.loads(r.content)
        elif type_id == '2':
            r = requests.get(LOCAL_URL+'news/news/', params=new_query_dict)
            content = json.loads(r.content)
        elif type_id == '3':
            r = requests.get(LOCAL_URL+'news/live/', params=new_query_dict)
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

