# -*- coding: utf-8 -*-

import json

from django.conf import settings
LOCAL_URL = settings.LOCAL_URL
from django.http import HttpResponse
from common.models import APIEncoder


class MapInterfaceObject(object):


    type_res = {
        "http_status": 200,
        "status": 'true',
        "data": [
            {
                "id": 1,
                "name": "推荐",
                "name_en": "tuijian",
                "listorder": 1,
                "status": 1
            },
            {
                "id": 2,
                "name": "资讯",
                "name_en": "zixun",
                "listorder": 2,
                "status": 1
            },
            {
                "id": 3,
                "name": "直播",
                "name_en": "zhibo",
                "listorder": 3,
                "status": 1
            },
            {
                "id": 4,
                "name": "精选",
                "name_en": "jingxuan",
                "listorder": 4,
                "status": 1
            },
            {
                "id": 5,
                "name": "数据",
                "name_en": "shuju",
                "listorder": 5,
                "status": 1
            }
        ],
        "meta": 'null',
        "msg": 'null',
        'code': '000000',
    }

    map_dict = {
        'per_page': 'number',
        'page': 'index',
        'tag_en': 'manual_tags',
        'keyword': 'machine_tags',
        's': 'content_html',
        'machine_class': 'machine_class',
        'is_recommend': 'is_recommend',
    }


    def get_mapping_query(self, data):
        """映射query"""
        res = {'number': 20}
        for k in data.keys():
            new_key = self.map_dict.get(k)
            if new_key:
                if data[k]:
                    res[new_key] = data[k]
        return res



    def get_http_res(self, data):
        content_type = '%s; charset=%s' % ("application/json",
                                           "UTF-8")
        return HttpResponse(json.dumps(data, cls=APIEncoder), content_type=content_type)

    def init_res(self, meta=None, data=[], msg='', http_status=200, status=True):
        res = {}
        res['meta'] = meta
        res['data'] = data
        res['msg'] = msg
        res['http_status'] = http_status
        res['status'] = status
        res['code'] = '000000'
        return res

    def get_res_list_data(self, data, type_id=2, type_name='zixun'):
        res = []
        for vals in data:
            new_vals = {}
            new_vals['id'] = str(vals.get('_id'))
            new_vals['news_types_id'] = int(type_id)
            new_vals['news_tags_tag_en'] = vals.get('manual_tags')
            # new_vals['news_tags_tag_en'] = type_name
            new_vals['title'] = vals.get('title')
            new_vals['from'] = vals.get('source')
            new_vals['from_url'] = vals.get('url')
            new_vals['thumb'] = vals.get('thumb')
            new_vals['keywords'] = vals.get('machine_tags')
            new_vals['desc'] = vals.get('machine_summary')
            new_vals['is_audit'] = 1
            new_vals['is_del'] = 0
            new_vals['is_hasdetails '] = str(vals.get('is_hasdetails', 1))
            new_vals['inputtime'] = str(vals.get('craw_time'))
            try:
                new_vals['friend_inputtime'] = str(vals.get('pub_time'))
            except Exception as e:
                new_vals['friend_inputtime'] = new_vals['inputtime']
            new_vals['updatetime'] = str(vals.get('craw_time'))
            new_vals['is_recommend'] = int(vals.get('is_recommend', 0))
            new_vals['is_col'] = 0
            new_vals['click_count'] = int(vals.get('click_count', 0))
            new_vals['machine_class'] = vals.get('machine_class')
            new_vals['hot_tag'] = vals.get('hot_tag', 0)

            # new_vals['id'] = str(vals.get('_id'))
            res.append(new_vals)
        return res


    def get_res_meta(self, meta):
        res={}
        res['total'] = meta.get('total_number')
        res['per_page'] = meta.get('number')
        res['current_page'] = meta.get('index')
        res['last_page'] = meta.get('index')+1
        if res['current_page'] == 1:
            res['next_page_url'] = LOCAL_URL + 'news/pagelist?page=%s'%str(res['current_page'] + 1)
            res['prev_page_url'] = None
        elif res['current_page'] == res['total']:
            res['next_page_url'] = None
            res['prev_page_url'] = LOCAL_URL + 'news/pagelist?page=%s' % str(res['current_page'] - 1)
        else:
            res['next_page_url'] = LOCAL_URL+'news/pagelist?page=%s'%str(res['current_page']+1)
            res['prev_page_url'] = LOCAL_URL+'news/pagelist?page=%s'%str*(res['current_page']-1)
        return res
