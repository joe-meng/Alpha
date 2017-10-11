#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from django.db.models import QuerySet
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
from common.utils import gen_page_info
from common.utils import log_exception
from ..models import Alert
from ..serializers import AlertSerializer


logger = logging.getLogger("use_info_ms")


class AlertView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取预警列表
        ---

        parameters:
            - name: class_display
              description: 是否分类显示(0:代表不分类, 1:代表分类显示)
              paramType: query
              required: false
            - name: date
              description: 日期
              paramType: query
              required: false
            - name: index
              description: 分页显示第几页
              paramType: query
              required: false
            - name: number
              description: 每页显示几条数据
              paramType: query
              required: false
            - name: descent
              description: 需要倒序的字段,用逗号分开,默认通过ID 正序
              paramType: query
              required: false
            - name: is_page
              description: 是否需要分页，default=1 ('0', '不需要分页')，('1', '需要分页')
              paramType: query
              required: false

        """
        query_dict = request.query_params.dict().copy()
        class_display = query_dict.pop('class_display', '0')
        date = query_dict.pop('date', None)
        user_id = request.user.id
        if user_id:
            filter_map = {'user_id': user_id}
        else:
            filter_map = {}
        if date:
            start = str(date)[:10] + ' 00:00:00'
            end = str(date)[:10] + ' 23:59:59'
            filter_map['created_at__lte'] = end
            filter_map['created_at__gte'] = start

        index, number, sort_tuple, descent = gen_page_info(query_dict)
        is_page = query_dict.pop('is_page', '1')

        # alert_objs = Alert.objects.filter(**filter_map).values('*').order_by(*sort_tuple).all()
        # alert_objs = Alert.objects.values_list('id', flat=True).distinct()
        query = Alert.objects.filter(**filter_map).order_by(*sort_tuple).all().query
        query.group_by = ['created_at']
        alert_objs = QuerySet(query=query, model=Alert)


        if is_page == '1':

            paginator = Paginator(alert_objs, number)

            try:
                pg = paginator.page(index)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                index = 1
                pg = paginator.page(index)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                index = paginator.num_pages
                pg = paginator.page(index)
            serializer = AlertSerializer(pg, many=True)
            res = serializer.data
            logger.info('正常返回分页:%s:' % (index))
            if str(class_display) == '1':
                res = group_res(serializer.data,)
            return BackstageHTTPResponse(
                                         data=res,
                                         message=u'正常返回分页').to_response()

        else:
            serializer = AlertSerializer(alert_objs, many=True)
            res = serializer.data
            logger.info('正常返回所有数据')
            if str(class_display) == '1':
                res = group_res(serializer.data)
            return BackstageHTTPResponse(
                data=res,
                message=u'正常返回所有数据').to_response()





def group_res(vals_lst):
    """分类数据"""
    res = {}
    group = []
    lst_res = []
    for vals in vals_lst:
        variety = vals['variety']
        if variety in group:
            res[variety].append(vals)
        else:
            res[variety] = [vals]
            group.append(variety)
    for key in res:
        lst_res.append({
            'text': key,
            'data': res[key],
        })
    return lst_res