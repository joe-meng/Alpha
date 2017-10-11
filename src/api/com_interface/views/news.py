#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-06-13

@author: Devin
"""
import logging
import json
import datetime


from common.models import BackstageHTTPResponse, PageInfo
from common.views import BackstageBaseAPIView
from common.utils import gen_like_filter_mongo
from common.utils import gen_page_info_mongo
from common.utils import get_mongo_id
from common.utils import log_exception
from backstage.views import news


logger = logging.getLogger("use_info_ms")


# class NewsViewList(news.NewsViewList):
class NewsViewList(BackstageBaseAPIView):

    def __init__(self, *args, **kwargs):
        super(NewsViewList, self).__init__(*args, **kwargs)
        self.col = self.db.news

    @log_exception
    def get(self, request):
        u"""
        获取所有的文章
        ---


        parameters:
            - name: machine_class
              description: 品目
              type: string
              paramType: query
              required: false
            - name: look_state
              description: 查看状态
              type: string
              paramType: query
              required: false
            - name: pub_state
              description: 发布状态
              type: string
              paramType: query
              required: false
            - name: push_state
              description: 推送状态
              type: string
              paramType: query
              required: false
            - name: pub_time
              description: 发布时间
              type: string
              paramType: query
              required: false
            - name: content_text
              description: 全文
              type: string
              paramType: query
              required: false
            - name: manual_tags
              description: 标签
              type: string
              paramType: query
              required: false
            - name: machine_tags
              description: 关键词,按英文逗号分开
              paramType: query
              required: false
            - name: top_tag
              description: 是否置顶
              type: string
              paramType: query
              required: false
            - name: time_start
              description: 开始时间
              type: string
              paramType: query
              required: false
            - name: time_end
              description: 结束时间
              type: string
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
        :param request:
        :return:
        """
        # query_dict = request.query_params.dict().copy()
        # is_page = query_dict.pop("is_page", "1")
        # msg = u"NewsView:get user:%s, request.data is:%s" % (
        #     request.user.username, str(query_dict))
        # logger.info(msg)
        # # col = self.db.news
        # time_start = query_dict.pop('time_start', None)
        # time_end = query_dict.pop('time_end', None)
        # manual_tags = query_dict.pop('manual_tags', None)
        # pub_time = query_dict.pop('pub_time', None)
        # index, number, sort_tuple, descent = gen_page_info_mongo(query_dict)
        # equal_key = ['content_html', 'machine_class', 'machine_tags']
        # if query_dict.get('machine_tags'):
        #     query_dict['machine_tags'] = query_dict['machine_tags'].split(',')[0]
        # new_query_dict = gen_like_filter_mongo(equal_key, query_dict)
        #
        # if manual_tags:
        #     new_query_dict['manual_tags'] = {'$all': manual_tags.split(',')}
        # if pub_time:
        #     date_start = datetime.datetime.strptime(pub_time + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        #     date_end = datetime.datetime.strptime(pub_time + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
        #     new_query_dict['$and'] = [{'pub_time': {'$gte': date_start}}, {'pub_time': {'$lte': date_end}}]
        # elif time_start and time_end:
        #     date_start = datetime.datetime.strptime(time_start, '%Y-%m-%d %H:%M:%S')
        #     date_end = datetime.datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
        #     new_query_dict['$and'] = [{'pub_time': {'$gte': date_start}}, {'pub_time': {'$lte': date_end}}]
        #
        # NEED_PAGE = "1"
        # if is_page == NEED_PAGE:
        #     pos = (index - 1) * number
        #     all_news_lst = self.col.find(new_query_dict).sort([('top_tag', -1), ('pub_time', -1), ('_id', -1)])
        #     # all_news_lst = self.col.find(new_query_dict).hint('news_top_time_desc')
        #     if pos > 0:
        #         news_lst = all_news_lst.skip(pos).limit(number)
        #     else:
        #         news_lst = all_news_lst.limit(number)
        #     llen = all_news_lst.count()
        #     num_pages = llen / number
        #     if llen % number != 0:
        #         num_pages = num_pages + 1
        #     logger.info(u'使用分页方式正常获取文章信息')
        #
        #     return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
        #                                  data=self.get_serializers_mongo(news_lst),
        #                                  pageinfo=PageInfo(index, number,
        #                                                    num_pages,
        #                                                    llen,
        #                                                    descent)
        #                                  ).to_response()
        # else:
        #     all_news_lst = self.col.find(new_query_dict).sort(sort_tuple)
        #
        #     logger.info(u'正常获取文章信息')
        #     return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
        #                                  data=self.get_serializers_mongo(all_news_lst), ).to_response()
        return news.NewsViewList().get(request)


class NewsView(BackstageBaseAPIView):

    @log_exception
    def get(self, request, pk):
        """
        通过主键获取新闻数据
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

        return news.NewsView().get(request, pk)
