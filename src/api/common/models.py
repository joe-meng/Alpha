#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-05-05

@author: Devin
"""
import json
from decimal import Decimal
from collections import OrderedDict
from datetime import datetime, date
from bson.objectid import ObjectId
from django.core.paginator import Page
from django.db import models

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


class PageInfo(object):
    def __init__(self, index, number, total_page, total_number, descent):
        self.index = index
        self.number = number
        self.total_page = total_page
        self.total_number = total_number
        self.descent = descent

    def dict(self):
        return dict(
            index=self.index,
            number=self.number,
            total_page=self.total_page,
            total_number=self.total_number,
            descent=self.descent
        )


class BackstageHTTPResponse(object):
    API_HTTP_CODE_NORMAL = '200'

    # 参数错误码
    API_HTTP_CODE_INVILID_PARAMS = '400'
    API_HTTP_CODE_NOT_FOUND = '404'
    API_HTTP_CODE_NOT_REAL_NAMED = '40003'

    API_HTTP_CODE_OTHER_ERROR = '10001'

    API_HTTP_CODE_NEWS_NOT_EXIST = '20001'

    API_HTTP_CODE_LOGIN_ERR = '30001'

    API_HTTP_CODE_NOT_LOGIN_ERR = '30002'
    API_HTTP_CODE_NO_PERMISSION = '30003'

    API_HTTP_CODE_FEEDBACK_CONTENT_NOT_EMPTY = '40001'

    CODE_DESCRIPTION = {
        API_HTTP_CODE_INVILID_PARAMS: u'传入参数错误',
        #  正常状态,打开就报错
        API_HTTP_CODE_NEWS_NOT_EXIST: u'id对应的消息不存在',

        API_HTTP_CODE_OTHER_ERROR: u'其他错误',

        API_HTTP_CODE_LOGIN_ERR: u'用户名或密码错误',

        API_HTTP_CODE_NOT_LOGIN_ERR: u"您无权限访问此api, 请先登录",
        API_HTTP_CODE_NO_PERMISSION: '您无权限操作',
        API_HTTP_CODE_NOT_FOUND: '未找到资源',

        API_HTTP_CODE_FEEDBACK_CONTENT_NOT_EMPTY: '意见反馈内容不能为空',
        API_HTTP_CODE_NOT_REAL_NAMED: '账户未实名',

    }

    def __init__(self, code='200', message="", description="", data=None,
                 pageinfo=None, extra=None):
        self.code = code
        self.message = message if message else self.CODE_DESCRIPTION.get(
            str(code), "")

        # self.description = description if isinstance(description, unicode) \
        #     else description.decode('utf-8')
        self.description = description

        self.data = data
        self.pageinfo = pageinfo
        self.extra = extra

    def to_dict(self):
        order_dict = OrderedDict(
            code=self.code,
            message=self.message,
            description=self.description,
            data=self.data,
        )
        if isinstance(self.pageinfo, PageInfo):
            order_dict.update(pageinfo=self.pageinfo.dict())
        elif isinstance(self.pageinfo, Page):
            order_dict.update(pageinfo=dict(
                index=self.pageinfo.number,
                number=self.pageinfo.paginator.per_page,
                total_page=self.pageinfo.paginator.num_pages,
                total_number=self.pageinfo.paginator.count,
            ))
        if self.extra:
            order_dict.update(**self.extra)
        return order_dict

    def to_json(self):
        ret = json.dumps(
            self.to_dict(), cls=APIEncoder,
            indent=4, ensure_ascii=False
        )
        return ret

    def to_response(self):
        content_type = '%s; charset=%s' % ("application/json",
                                               "UTF-8")
        return HttpResponse(self.to_json(), content_type=content_type)


class APIEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return str(obj).replace('T', ' ')
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, bytes):
            return obj.decode('ascii')
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class KVObject(models.Model):
    """
    键值对储存
    """
    k = models.CharField(max_length=128, primary_key=True)
    v = models.TextField(null=True)

    class Meta:
        db_table = 'kv_object'
