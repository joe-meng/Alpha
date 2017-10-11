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


logger = logging.getLogger("use_info_ms")


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
            - name: content_html
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
            - name: source
              description: 来源
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
        query_dict = request.query_params.dict().copy()
        is_page = query_dict.pop("is_page", "1")
        msg = u"NewsView:get user:%s, request.data is:%s" % (
                  request.user.username, str(query_dict))
        logger.info(msg)
        # col = self.db.news
        time_start = query_dict.pop('time_start', None)
        time_end = query_dict.pop('time_end', None)
        manual_tags = query_dict.pop('manual_tags', None)
        pub_time = query_dict.pop('pub_time', None)
        index, number, sort_tuple, descent = gen_page_info_mongo(query_dict)
        equal_key = ['content_html', 'machine_tags']
        if query_dict.get('machine_tags'):
            query_dict['machine_tags'] = query_dict['machine_tags'].split(',')[0]
        new_query_dict = gen_like_filter_mongo(equal_key, query_dict)

        if manual_tags:
            new_query_dict['manual_tags'] = {'$all': manual_tags.split(',')}
        if pub_time:
            date_start = datetime.datetime.strptime(pub_time+' 00:00:00', '%Y-%m-%d %H:%M:%S')
            date_end = datetime.datetime.strptime(pub_time+' 23:59:59', '%Y-%m-%d %H:%M:%S')
            new_query_dict['$and'] = [{'pub_time': {'$gte': date_start}}, {'pub_time': {'$lte': date_end}}]
        elif time_start and time_end:
            date_start = datetime.datetime.strptime(time_start, '%Y-%m-%d %H:%M:%S')
            date_end = datetime.datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
            new_query_dict['$and'] = [{'pub_time': {'$gte': date_start}}, {'pub_time': {'$lte': date_end}}]
        NEED_PAGE = "1"
        if is_page == NEED_PAGE:
            pos = (index-1) * number
            # all_news_lst = self.col.find(new_query_dict).hint('123')
            if descent == 'craw_time':
                all_news_lst = self.col.find(new_query_dict).hint('news_top_time_desc')
            elif descent == 'click_count':
                all_news_lst = self.col.find(new_query_dict).hint('news_top_click_desc')
            else:
                all_news_lst = self.col.find(new_query_dict).hint('news_top_pub_desc')
            if pos > 0:
                news_lst = all_news_lst.skip(pos).limit(number)
            else:
                news_lst = all_news_lst.limit(number)
            llen = all_news_lst.count()
            num_pages = llen / number
            if llen % number != 0:
                num_pages = num_pages+1
            logger.info(u'使用分页方式正常获取文章信息')

            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                   data=self.get_serializers_mongo(news_lst),
                                   pageinfo=PageInfo(index, number,
                                                     num_pages,
                                                     llen,
                                                     descent)
                                   ).to_response()
        else:
            all_news_lst = self.col.find(new_query_dict).sort(sort_tuple)

            logger.info(u'正常获取文章信息')
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                        data=self.get_serializers_mongo(all_news_lst),).to_response()


    @log_exception
    def put(self, request):
        """
        通过主键批量编辑修改
        ---

        parameters:

            - name: id_lists
              description: 数据id列表,用逗号隔开
              type: integer
              paramType: form
              required: true
            - name: id_lists
              description: 数据id列表,用逗号隔开
              type: integer
              paramType: form
              required: true
            - name: look_state
              description: 查看状态(0未查看,1代表已查看)
              type: string
              required: false
            - name: pub_state
              description: 发布状态(0代表未发布,1代表已发布)
              type: string
              required: false
            - name: is_rmd
              description: 是否推荐(0代表未发布,1代表已发布)
              type: string
              required: false

        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 403
              message: Insufficient rights to call this procedure
        """
        post_data = self.request_data(request)
        msg = u"NewsView:put request.data is:%s" % str(post_data)
        logger.info(msg)
        post_data.pop('_id', None)
        id_list = post_data.get('id_lists', '')
        look_state = post_data.get('look_state', None)
        pub_state = post_data.get('pub_state', None)
        is_rmd = post_data.get('is_rmd', None)
        vals = {}

        if not id_list:
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=u"数据_id列表为必填项").to_response()
        if look_state and look_state not in ['0', '1']:
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=u"查看状态格式错误,必须为0或1").to_response()
        elif look_state:
            vals['look_state'] = look_state

        if pub_state and pub_state not in ['0', '1']:
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=u"发布状态格式错误,必须为0或1").to_response()
        elif pub_state:
            vals['pub_state'] = pub_state

        if is_rmd and is_rmd not in ['0', '1']:
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=u"是否推荐格式错误,必须为0或1").to_response()
        elif is_rmd:
            vals['is_rmd'] = is_rmd
        res = []
        # selfcol = self.db.news
        if vals:
            for i in id_list:
                _id = get_mongo_id(i)
                news_obj = self.col.find_one({'_id': _id})
                if not news_obj:
                    logger.info(u"NewsView:id %s ID对应的消息不存在",
                                _id)
                    # return BackstageHTTPResponse(
                    #     BackstageHTTPResponse.API_HTTP_CODE_NEWS_NOT_EXIST,
                    # ).to_response()
                else:
                    if post_data:
                        self.col.update({"_id": _id}, {"$set": vals})
                    news_obj = self.col.find_one({'_id': _id})
                    logger.info(u'通过主键修改news成功')
                    news_obj['_id'] = str(news_obj['_id'])
                    res.append(news_obj)

        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=res).to_response()


    @log_exception
    def delete(self, request):
        """
        通过主键批量删除咨询
        ---

        parameters:

            - name: id_lists
              description: 数据id列表,用逗号隔开
              type: string
              paramType: form
              required: true

        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 403
              message: Insufficient rights to call this procedure
        """
        # post_data = self.request_data(request)
        post_data = request.data.copy()
        msg = u"NewsView:delete request.data is:%s" % str(post_data)
        logger.info(msg)
        id_list = post_data.get('id_lists', '')
        if not id_list:
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=u"数据_id列表为必填项").to_response()
        # col = self.db.news
        res = []
        for i in id_list.split(','):
            _id = get_mongo_id(i)
            key = self.col.find_one({'_id': _id})
            if key:
                # key['_id'] = str(key['_id'])
                self.col.find_one_and_delete({"_id": _id})
                res.append(key)
            else:
                logger.info('_id:%s, 对应的数据不存在'%_id)
        return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                     data=res,
                                     message=u'批量删除成功').to_response()


    def post(self, request):
        """
        添加一篇文章
        ---

        parameters:
            - name: title
              description: 标题
              type: string
              paramType: form
              required: true
            - name: source
              description: 来源
              type: string
              paramType: form
              required: false
            - name: pub_time
              description: 发布时间
              type: string
              paramType: form
              required: true
            - name: machine_tags
              description: 关键词
              type: string
              paramType: form
              required: false
            - name: machine_class
              description: 品目
              type: string
              paramType: form
              required: false
            - name: machine_summary
              description: 摘要
              type: string
              paramType: form
              required: false
            - name: content_html
              description: 全文
              type: string
              paramType: form
              required: true
            - name: manual_tags
              description: 手动tag(传列表json字符串)
              type: string
              paramType: form
              required: false
            - name: top_tag
              description: 置顶或取消置顶(0代表取消置顶, 1代表置顶)
              type: string
              paramType: form
              required: false
            - name: is_rmd
              description: 是否推荐(0代表未推荐,1代表推荐)
              type: string
              paramType: form
              required: false


        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 403
              message: Insufficient rights to call this procedure
        """

        post_data = self.request_data(request)
        post_data.pop('craw_time', None)
        vals = {'look_state': '0', 'pub_state': '0', 'push_state': '0',
                'source': u'有色在线', 'machine_tags': '', 'machine_class': '',
                'machine_summary': '', 'manual_tags': [], 'content_text': '',
                'top_tag': '0', 'craw_time': datetime.datetime.now(),
                'pub_time': datetime.datetime.now(), }
        logger.info(u'添加一篇文章%s' %post_data)
        if post_data.get('pub_time'):
            pub_time = post_data['pub_time'].replace('T', ' ')
            post_data['pub_time'] = datetime.datetime.strptime(pub_time[:19], '%Y-%m-%d %H:%M:%S')
        if not post_data.get('title'):
            logger.info(u'参数错误, 标题必填')
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=u'标题必填').to_response()
        if not post_data.get('pub_time'):
            logger.info(u'参数错误,发布时间必填')
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=u'发布时间必填').to_response()
        if not post_data.get('content_html'):
            logger.info(u'参数错误, 正文必填')
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=u'正文必填').to_response()
        vals['content_text'] = post_data.get('content_html')
        # if post_data.get('manual_tags'):
        #     post_data['manual_tags'] = post_data.get('manual_tags')
        vals.update(post_data)

        _id = self.col.insert(vals)
        vals['_id'] = _id
        logger.info(u'成功添加一篇文章')
        return BackstageHTTPResponse(data=vals,
                                     message=u'成功添加一篇文章').to_response()


class NewsView(BackstageBaseAPIView):

    def __init__(self, *args, **kwargs):
        super(NewsView, self).__init__(*args, **kwargs)
        self.col = self.db.news


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

        query_dict = request.query_params.dict().copy()
        query_dict.pop('_id', None)
        _id = get_mongo_id(pk)
        logger.info(u'通过id:%s获取消息数据'%_id)
        # col = self.db.news
        news_obj = self.col.find_one({'_id': _id})
        logger.info(u'正常通过主键获取消息数据成功')
        if news_obj:
            old_click = news_obj.get('click_count', 0)
            self.col.update({'_id': _id}, {"$set": {'click_count': int(old_click)+1}})

            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                               data=news_obj).to_response()

        else:
            logger.info(u"NewsView:id %s ID对应的消息不存在",
                        _id)
            return BackstageHTTPResponse(
                BackstageHTTPResponse.API_HTTP_CODE_NEWS_NOT_EXIST,
            ).to_response()

    @log_exception
    def put(self, request, pk):
        """
        通过主键编辑修改
        ---

        parameters:

            - name: pk
              description: 数据id
              type: string
              paramType: path
              required: true
            - name: title
              description: 标题
              type: string
              required: false
            - name: source
              description: 来源
              type: string
              required: false
            - name: pub_time
              description: 发布时间
              type: string
              required: false
            - name: machine_tags
              description: 关键词
              type: string
              required: false
            - name: machine_class
              description: 品目
              type: string
              required: false
            - name: machine_summary
              description: 摘要
              type: string
              required: false
            - name: content_html
              description: 全文
              type: string
              required: false
            - name: look_state
              description: 处理状态
              type: string
              required: false
            - name: pub_state
              description: 发布状态
              type: string
              required: false
            - name: push_state
              description: 推送状态
              type: string
              required: false
            - name: manual_tags
              description: 手动tag(传列表json字符串)
              type: string
              required: false
            - name: top_tag
              description: 置顶或取消置顶(0代表取消置顶, 1代表置顶)
              type: string
              required: false
            - name: thumb
              description: 焦点图url
              type: string
              required: false
            - name: is_rmd
              description: 是否推荐(0代表未推荐,1代表推荐)
              type: string
              required: false
            - name: pdf_url
              description: pdf文件的url
              type: string
              required: false


        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 403
              message: Insufficient rights to call this procedure
        """
        post_data = self.request_data(request)
        msg = u"NewsView:put request.data is:%s" % str(post_data)
        logger.info(msg)
        post_data.pop('_id', None)
        top_tag = post_data.get('top_tag', None)
        if post_data.get('pub_time'):
            pub_time = post_data['pub_time'].replace('T', ' ')
            post_data['pub_time'] = datetime.datetime.strptime(pub_time[:19], '%Y-%m-%d %H:%M:%S')
        if not post_data.get('look_state'):
            post_data['look_state'] = '1'
        _id = get_mongo_id(pk)
        if not _id:
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                        message=u"数据_id为必填项").to_response()
        # col = self.db.news
        news_obj = self.col.find_one({'_id': _id})
        if not news_obj:
            logger.info(u"NewsView:id %s ID对应的消息不存在",
                        _id)
            return BackstageHTTPResponse(
                    BackstageHTTPResponse.API_HTTP_CODE_NEWS_NOT_EXIST,
                ).to_response()
        else:
            # if top_tag:
            #     post_data['top_tag'] = int(top_tag)
            # if post_data.get('manual_tags'):
            #     self.db.tag_ware.upsert()
            #     new_tags = post_data.get('manual_tags')
            #     tag_vals = self.db.tag_ware.find_one().get('tag')
            #     new_tag_vals = set(tag_vals) | set(new_tags)
            #     self.db.tag_ware.update({}, {'tag': list(new_tag_vals)})
            #     post_data['manual_tags'] = new_tags
            if post_data:
                self.col.update({"_id": _id}, {'$set': post_data})

            news_obj = self.col.find_one({'_id': _id})
            logger.info(u'通过主键修改news成功')
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                   data=news_obj).to_response()

    @log_exception
    def delete(self, request, pk):
        """
        通过主键删除咨询
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
        _id = get_mongo_id(pk)
        if not _id:
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=u"数据_id为必填项").to_response()
        # col = self.db.news
        res = self.col.find_one({"_id": _id})
        if res:
            self.col.find_one_and_delete({"_id": _id})
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_NORMAL,
                                    message=u'删除成功',
                                    data=res).to_response()
        else:
            return BackstageHTTPResponse(BackstageHTTPResponse.API_HTTP_CODE_INVILID_PARAMS,
                                         message=u"数据_id对应数据不存在").to_response()