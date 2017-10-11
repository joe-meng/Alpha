# -*- coding: utf-8 -*-
import datetime
import hashlib
import scrapy
from scrapy.http import Request
from websitespider.items import SpiderItems
from websitespider.utils.db import MongoHandler

class EnanchuSpider(scrapy.Spider):
    name = "enanchu"
    host = 'http://www.enanchu.com'
    allowed_domains = ["enanchu.com"]
    handler = MongoHandler()
    def start_requests(self):
        urls = [
            'http://www.enanchu.com/news/futures/1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        * 解析新闻列表的第一页内容
        """
        url_list = []
        cur_url = response.url
        url_list = response.xpath("//h3/a/@href").extract()
        title_list = response.xpath("//h3/a/text()").extract()
        for url in url_list:
            url = self.host+url
            _id = hashlib.sha256(url.encode('utf-8')).hexdigest()
            if self.handler.check_exist("news", {"_id": _id}):
                # 如果在数据库中已经存在  直接跳过
                continue
            else:
                print("url",url)
                # 处理数据库中不存在的
                yield Request(
                    url,
                    meta={
                        'source': '南储商务网',
                        '_id': _id,
                    },
                    callback=self.parse_content,
                    dont_filter=False
                )

    def parse_content(self, response):
        # 解析新闻详情页面的内容
        now = datetime.datetime.now()
        title = response.xpath("//div[@id='news_in_one_left_title']/h1/text()").extract()[0]
        sub_title = response.xpath("//div[@id='news_in_one_left_time']/text()").extract()[0]
        try:
            sub_list = sub_title.split(" ")
            website = sub_list[0]
            pub_time = sub_list[2] + sub_list[3]
        except:
            website = ''
            pub_time = ''
        content_html = "".join(response.xpath("//div[@id='news_in_one_left_text']").extract())
        txtcont_text = "".join(response.xpath("//div[@id='news_in_one_left_text']/p/text()").extract())
        insert_info = {
            "title" : title,
            "_id" : response.meta['_id'],
            "url" : response.url,
            "website" : website,
            "pub_time" : pub_time,
            "content_html" : content_html,
            "source": response.meta['source'],
            "craw_time" : now,
            "content_text" : txtcont_text,
        }
        _id = self.handler.insert_one('news', insert_info)
        yield SpiderItems(
            **{"_id":_id}
        )
