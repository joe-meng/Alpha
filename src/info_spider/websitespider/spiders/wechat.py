# -- coding: utf-8 --
import json
import logging
import pprint
from datetime import datetime
import re
import scrapy
from bson import ObjectId

from websitespider.exceptions import BannedException
from websitespider.items import WechatItem
from websitespider.utils.utils import unescape_html


class WechatSpider(scrapy.Spider):
    """
    文章分为主推送(带缩略图)文章,以及次级推送文章。一次推送只能有一个主推送,可以包括多个次级推送。
    爬取时先把次级推送信息储存在 sub_posts 字段中, 在 mongo pipeline 识别是否存在子推送, 如存在则继续爬取次级推送, 单独存一条 mongo 记录, 爬到的次级推送会在主 mongo 记录的 sub_posts 对应记录中加一个 id 字段作为次级推送已下载标识
    """
    name = "wechat"

    # self.db 是 mongo pipeline 中赋值的
    # self.username 是命令行中给的
    def __init__(self, name=None, **kwargs):
        if 'username' not in kwargs:
            raise Exception('需要提供微信公众号用户名')
        super(WechatSpider, self).__init__(name, **kwargs)

    def start_requests(self):
        search_url = 'http://weixin.sogou.com/weixin?type=1&query=%s&ie=utf8&s_from=input&_sug_=y&_sug_type_=' % self.username
        yield scrapy.Request(url=search_url, callback=self.parse_search, dont_filter=True)

    def parse_search(self, response):
        list_url = response.xpath("//p[@class='tit']/a/em[text()='%s']/../@href" % self.username).extract_first('')

        if not list_url:
            banned = '验证码' in response.css('.p3').extract_first('')
            if banned:
                self.log('爬虫被发现'.center(80, '-'), logging.CRITICAL)
                raise BannedException('爬虫被发现'.center(80, '-'))
            else:
                self.log('未知错误'.center(80, '-'), logging.CRITICAL)

        self.log('公众号: %s 搜索页面解析出列表地址: %s' % (self.username, list_url), logging.INFO)
        yield scrapy.Request(url=list_url, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        # 用原生 re 取 js 中的 JSON, 避免自动 html escape
        article_list = re.findall(r'var msgList = (.*);', response.text)

        if not article_list:
            banned = '跳转中' in response.css('#loading').extract_first('')
            if banned:
                self.log('爬虫被发现'.center(80, '-'), logging.CRITICAL)
                raise BannedException('爬虫被发现'.center(80, '-'))
            else:
                self.log('未知错误'.center(80, '-'), logging.CRITICAL)
                raise Exception('未知错误'.center(80, '-'))

        article_list = article_list[0]
        try:
            # load 时对 JSON 所有值进行 html unescape
            article_list = json.loads(article_list, object_hook=unescape_html)['list']
            self.log('公众号: %s 列表页面解析出最新文章:\n%s' % (self.username, pprint.pformat([a['app_msg_ext_info']['title'] for a in article_list])), logging.INFO)
        except:
            self.log('公众号: %s 列表页面解析失败, url: %s' % (self.username, response.url), logging.ERROR)
            raise

        for article in article_list:
            wechat_post_id = self.username + str(article['comm_msg_info']['id'])
            meta = {
                'item': {
                    'thumb': [article['app_msg_ext_info']['cover']],
                    'wechat_post_id': wechat_post_id,
                    'website': article['app_msg_ext_info']['source_url'],
                    'sub_posts': article['app_msg_ext_info']['multi_app_msg_item_list'],
                    'main_post_id': None,
                    'sub_post_index': None,
                }
            }

            self.log('公众号: %s 列表页面解析出主推文: %s' % (wechat_post_id, article['app_msg_ext_info']['title']), logging.INFO)

            # 根据 wechat id 去重
            # self.db 是 mongo_pipeline 中添加的属性
            existing_post = self.db.find_one({'wechat_post_id': wechat_post_id})
            if existing_post:
                existing_sub_posts = existing_post.get('sub_posts', [])
                if all([i.get('id', None) for i in existing_sub_posts]):
                    self.log('公众号: %s 主推文及其子推文已下载过: %s' % (wechat_post_id, article['app_msg_ext_info']['title']), logging.INFO)
                    continue
                else:
                    meta['main_post_id'] = existing_post['_id']
                    for index, sub_post in enumerate(existing_sub_posts):
                        if isinstance(sub_post, ObjectId):
                            continue
                        self.log('公众号: %s 列表页面解析出子推文: %s' % (wechat_post_id, sub_post['title']), logging.INFO)
                        meta['sub_post_index'] = index
                        yield scrapy.Request(url=response.urljoin(sub_post['content_url']), callback=self.parse_detail, meta=meta)
            else:
                yield scrapy.Request(url=response.urljoin(article['app_msg_ext_info']['content_url']), callback=self.parse_detail, meta=meta)

    def parse_detail(self, response):
        """
        :param response: scrapy.http.Response
        :return:
        """
        item = {
            'title': response.css("#activity-name::text").extract_first('').strip(),
            'source': response.css(".rich_media_meta_nickname::text").extract_first('').strip(),
            'url': response.url,
            'content_html': response.css(".rich_media_content").extract_first('').strip(),
            'author': response.css(".rich_media_meta_text::text")[1:].extract_first('').strip(),
            'pub_time': self.format_pub_time(response.css("#post-date::text").extract_first('').strip()),
            'craw_time': datetime.now(),
            'wechat_username': self.username,
        }
        item.update(response.meta.get('item', {}))
        yield WechatItem(**item)

    def format_pub_time(self, pub_time):
        return datetime.strptime(pub_time, "%Y-%m-%d")
