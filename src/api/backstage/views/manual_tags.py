#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-06-13

@author: Devin
"""
import logging
from bson.objectid import ObjectId

from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
from common.utils import log_exception

logger = logging.getLogger("use_info_ms")


class ManualTagView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        u"""
        获取所有标签
        ---

        :param request:
        :return:
        """
        col = self.db.tag_ware
        vals = col.find()
        key = [item['total'] for item in vals]
        # vals = col.find_one()
        res = {'tag': key}
        logger.info('获取所有标签')
        return BackstageHTTPResponse(message=u'成功获取所有标签', data=res).to_response()

    @log_exception
    def post(self, request):
        """
        新增一个标签
        ---
        parameters:
            - name: name
              description: 名称
              type: string
              paramType: form
              required: true
            - name: tag
              description: 标签
              type: string
              paramType: form
              required: true
            - name: type
              description: 类型
              type: string
              paramType: form
              required: true

        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 403
              message: Insufficient rights to call this procedure
        """
        collection = self.db.tag_ware
        data = self.request_data(request)
        name = data['name']
        tag = data['tag']
        tag_type = data['type']
        if collection.find_one({'tag': tag}):
            logger.info('标签已存在')
            return BackstageHTTPResponse(message=u'标签已存在', data={}).to_response()
        else:
            total = '%s-%s-%s' % (name, tag, tag_type)
            document = {'tag': tag, 'name': name, 'type': tag_type, 'total': total}
            collection.insert_one(document)
            return BackstageHTTPResponse(message=u'添加标签成功', data=document).to_response()

    @log_exception
    def put(self, request):
        """
        修改标签
        ---
        parameters:
            - name: _id
              description: 标签_id
              type: string
              paramType: form
              required: true
            - name: name
              description: 名称
              type: string
              paramType: form
              required: true
            - name: tag
              description: 标签
              type: string
              paramType: form
              required: true
            - name: type
              description: 类型
              type: string
              paramType: form
              required: true

        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 403
              message: Insufficient rights to call this procedure
        """
        collection = self.db.tag_ware
        data = self.request_data(request)
        _id = data['_id']
        name = data['name']
        tag = data['tag']
        tag_type = data['type']
        total = '%s-%s-%s' % (name, tag, tag_type)
        document = {'name': name, 'tag': tag, 'type': tag_type, 'total': total}
        collection.update({'_id': ObjectId(_id)}, {'$set': document})
        document['_id'] = _id
        return BackstageHTTPResponse(message=u'修改标签成功', data=document).to_response()

    def delete(self, request):
        """
        删除标签
        ---
        parameters:
            - name: _id
              description: 标签_id
              type: string
              paramType: form
              required: true

        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 403
              message: Insufficient rights to call this procedure
        """
        collection = self.db.tag_ware
        data = self.request_data(request)
        _id = data['_id']
        collection.remove({'_id': ObjectId(_id)})
        return BackstageHTTPResponse(message=u'删除标签成功', data={}).to_response()


class TagListView(BackstageBaseAPIView):

    @log_exception
    def get(self, request):
        """
        分页获取标签列表
        ---
        parameters:
            - name: index
              description: 页数
              type: integer
              paramType: query
              required: false
            - name: number
              description: 每页条数
              type: string
              paramType: query
              required: false
            - name: name
              description: 标签名称
              type: string
              paramType: query
              required: false
            - name: tag
              description: 标签
              type: string
              paramType: query
              required: false
            - name: type
              description: 标签类型
              type: string
              paramType: query
              required: false

        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 403
              message: Insufficient rights to call this procedure
        """
        page = request.GET.get('index') or 1
        page = int(page)
        per_page = request.GET.get('number') or 20
        per_page = int(per_page)
        limit = int(per_page)
        skip = (int(page) - 1) * int(per_page)
        name = request.GET.get('name')
        tag = request.GET.get('tag')
        tag_type = request.GET.get('type')
        query = {}
        if name:
            query['name'] = name
        if tag:
            query['tag'] = tag
        if tag_type:
            query['type'] = tag_type
        collection = self.db.tag_ware
        count = collection.find(query).count()
        data = collection.find(query).limit(limit).skip(skip)
        pages = count // limit + bool(count % limit)
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=list(data),
                                     pageinfo=PageInfo(page, per_page,
                                                       pages,
                                                       count,
                                                       '')
                                     ).to_response()


class TagView(BackstageBaseAPIView):

    @log_exception
    def get(self, request, pk):
        """
        分页获取标签列表
        ---
        parameters:
            - name: pk
              description: 数据id
              type: string
              paramType: path
              required: true

        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 403
              message: Insufficient rights to call this procedure
        """
        collection = self.db.tag_ware
        doc = collection.find_one({'_id': ObjectId(pk)})
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=doc).to_response()
