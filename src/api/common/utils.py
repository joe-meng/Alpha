#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@date: 2016-05-06

@author: Devin
"""
import logging
import random
import re
from bson.objectid import ObjectId
import string
import traceback
from datetime import datetime
from functools import wraps
from io import BytesIO
# from urllib import urlencode
# from urlparse import urlparse, parse_qsl, ParseResult


from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import QueryDict
import pymongo
from rest_framework.views import APIView

from .models import BackstageHTTPResponse
import uuid

logger = logging.getLogger("use_info_ms")


def gen_zero_time():
    '''
    生成当天零点时间
    '''
    today = datetime.today()
    b = datetime(today.year, today.month, today.day, 0, 0, 0)
    return b


def gen_topic_url(args, sep='/'):
    if "" in args:
        args.remove("")
    if None in args:
        args.remove(None)
    return sep.join(args)


def gen_filter_dict(user):
    filter_dict = {}
    if user.is_superuser:
        return filter_dict
    else:
        filter_dict.update(user__id=user.id)
        return filter_dict


def gen_sort_tuple(model, query_map=dict()):
    columns = model._meta.get_all_field_names()
    descent = query_map.pop("descent", None)
    sort_tuple = []
    if descent:
        sort_tuple = ["-%s" % x for x in descent.split(",") if x in columns]
    if not sort_tuple:
        sort_tuple = ['id']
    sort_tuple = tuple(sort_tuple)
    return sort_tuple


def gen_like_filter(exact_keys=[], query_map=dict(), user=AnonymousUser()):
    """
    生成filter, 使用
    :param exact_keys: 等于的KEY
    :param query_map: 所有的健值
    :return: 新的query dict
    """
    query_dict = query_map.copy()
    new_query_dict = dict()
    for k, v in query_dict.iteritems():
        k = k.replace(".", "__")
        if k in exact_keys:
            new_query_dict['%s' % k] = v
        else:
            new_query_dict['%s__icontains' % k] = v
    if user.is_superuser:
        return new_query_dict

    if user.is_admin():
        return new_query_dict

    if user.is_super_admin():
        return new_query_dict

    if user.is_authenticated():
        new_query_dict['user__id'] = user.id
        return new_query_dict

    return new_query_dict

def gen_page_info(query_map=dict()):
    """
    生成page, index ,order by
    :param query_map:
    :return:
    """
    from django.conf import settings
    descent = query_map.pop("descent", None)
    sort_tuple = ["id"]
    if descent:
        sort_tuple = ["-%s" % x.replace(".", "__") for x in descent.split(",")]
    sort_tuple = tuple(sort_tuple)

    number = int(
        query_map.pop("number", settings.REST_FRAMEWORK.get("PAGE_SIZE")))
    index = int(query_map.pop("index", 1))
    return index, number, sort_tuple, descent


def tuple2dict(t_tuple):
    t_dict = dict()
    map(lambda x: t_dict.update({x[0]: x[1]}), t_tuple)
    return t_dict


# def url_add_params(url, **params):
#     """ 在网址中加入新参数 """
#     pr = urlparse(url)
#     query = dict(parse_qsl(pr.query))
#     query.update(params)
#     prlist = list(pr)
#     prlist[4] = urlencode(query)
#     return ParseResult(*prlist).geturl()


def log_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            query = {}
            if len(args) >= 2 and isinstance(args[1], APIView) and args[1].method == 'GET':
                query = args[1].query_params
            body = {}
            if len(args) >= 2 and isinstance(args[1], APIView) and args[1].method in ('PUT', 'POST', 'PATCH'):
                body = args[1].data
            logger.info('processing request: %s, %s. query: %s, body: %s' % (str(args), str(kwargs), query, body))
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.info(u"catch unhandled exception: %s ",
                        str(traceback.format_exc()))
            traceback.print_exc()
            return BackstageHTTPResponse(
                BackstageHTTPResponse.API_HTTP_CODE_OTHER_ERROR,
                message=str(e),
                description=u"捕获到未处理的异常,%s" %
                str(traceback.format_exc())).to_response()


    return wrapper


def wrapperdata(func):
    @wraps
    def wrapper(*args, **kwargs):
        cls = args[0]
        request = args[1]
        if not request.method in ['PUT', 'POST']:
            return func(*args, **kwargs)
        data_dict = request.data
        if isinstance(data_dict, QueryDict):
            data_dict = data_dict.dict()
            request.data = data_dict
        return func(*args, **kwargs)

    return wrapper


def load_note(vals):
    res, use = [], ''
    try:
        use, oth = vals.split('---')
        content = oth.split('responseMessages')[0].strip()
        para_lst = content.split('- ')[1:]
        # print len(para_lst), para_lst[0]
        for k in para_lst:
            content_lst = k.split('\n')
            para = {}
            for i in range(len(content_lst)):
                line = content_lst[i]
                line_lst = line.split(':')
                if len(line_lst) == 2:
                    line_key = line_lst[0].strip()
                    line_value = line_lst[1].strip()
                    if line_value == '>':
                        para_vals = ''
                        for m in range(1, len(content_lst) - i):
                            if '-' in content_lst[m + i]:
                                i += m
                                break
                            para_vals += content_lst[m + i].strip()
                        para[line_key] = para_vals
                        # res.append(para)
                        continue
                    else:
                        para[line_key] = line_value
            res.append(para)
    except Exception as e:
        # import traceback
        logger.error('load note err===')
    return (use, res)



def get_update_dict(data, keys):
    res = {}
    for key in keys:
        if key in data.keys():
            res[key] = data.get(key, '')
    return res


def update_by_dict(md, data):
    for key in data:
        setattr(md, key, data.get(key))
    return md


def get_uuid():
    return str(uuid.uuid1())[:8]


def gen_page_info_mongo(query_map=dict()):
    """
        生成page, index ,order by
        :param query_map:
        :return:
        """
    descent = query_map.pop("descent", 'craw_time')
    sort_tuple = [("pub_time", pymongo.DESCENDING), ("_id", pymongo.DESCENDING), ('top_tag', pymongo.DESCENDING)]
    # sort_tuple = [('top_tag', pymongo.DESCENDING), ("pub_time", pymongo.DESCENDING)]
    # sort_tuple = [('top_tag', pymongo.DESCENDING)]
    # if descent:
    #     for i in descent.split(','):
    #         sort_tuple.append((i, pymongo.DESCENDING))
    sort_tuple = tuple(sort_tuple)

    number = int(
        query_map.pop("number", settings.REST_FRAMEWORK.get("PAGE_SIZE")))
    index = int(query_map.pop("index", 1))
    return index, number, sort_tuple, descent


def gen_like_filter_mongo(exact_keys=[], query_map=dict(), user=AnonymousUser()):
    """
    生成filter, 使用
    :param exact_keys: 模糊查询的KEY
    :param query_map: 所有的健值
    :return: 新的query dict
    """
    query_dict = query_map.copy()
    new_query_dict = dict()

    for k, v in query_dict.items():
        k = k.replace(".", "__")
        if k in exact_keys:
            new_query_dict[k] = re.compile('.*%s.*'%v)
        else:
            new_query_dict[k] = v


    return new_query_dict

def get_mongo_id(_id):
    if type(_id) == ObjectId:
        return _id
    elif len(_id) == 24:
        return ObjectId(_id)
    elif len(_id) == 64:
        return _id


from rest_framework.schemas import SchemaGenerator
from rest_framework.compat import coreapi, urlparse
import yaml

class AlphaSchemaGenerator(SchemaGenerator):

    # map_of_swagger = {'query': }

    def get_link(self, path, method, view):
        """
        Return a `coreapi.Link` instance for the given endpoint.
        """
        description = self.get_description(path, method, view)

        fields = []
        if '---' not in description:
            fields += self.get_path_fields(path, method, view)
            fields += self.get_serializer_fields(path, method, view)
            fields += self.get_pagination_fields(path, method, view)
            fields += self.get_filter_fields(path, method, view)

        if description:
            vals = list(yaml.load_all(description))
            description, para_lst = vals[0], vals[1]
            if para_lst and para_lst.get('parameters'):
                for para in para_lst['parameters']:
                    fields.append(coreapi.Field(
                        name=para['name'],
                        required=para['required'],
                        location=para.get('paramType', 'query'),
                        description=para['description'],
                        type=para.get('type', 'string')
                    ))

        if fields and any([field.location in ('form', 'body') for field in fields]):
            # encoding = self.get_encoding(path, method, view)
            encoding = 'multipart/form-data'
        else:
            encoding = None


        if self.url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urlparse.urljoin(self.url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=description
        )
