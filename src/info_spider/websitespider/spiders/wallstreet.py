# -*- coding: utf-8 -*-
import datetime
import hashlib
import scrapy
import time
import json
import requests
from scrapy.http import Request
from websitespider.items import SpiderItems
from websitespider.utils.db import MongoHandler

class WallStreetSpider(scrapy.Spider):
    name = "wallstreet"
    host = 'https://wallstreetcn.com'
    handler = MongoHandler()
    def start_requests(self):
        urls = [
            "https://wallstreetcn.com/news/global",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        * 解析新闻列表的第一页内容
        """
        url_list = response.xpath("//div[@class='wscn-tabs__content']/div[@class='wscn-tab-pane' and position()=1]/div/div/a/@href").extract()
        for url in url_list:

            if url.startswith("https"):
                continue
            else:
                url = self.host+url
                _id = hashlib.sha256(url.encode('utf-8')).hexdigest()
                if self.handler.check_exist("news", {"_id": _id}):
                    continue
                else:
                    yield Request(
                        url,
                        meta={
                            'url': url,
                            '_id': _id,
                        },
                        callback=self.parse_content,
                        dont_filter=False
                    )

    def parse_content(self, response):
        # 解析新闻详情页面的内容

        now = datetime.datetime.now()
        title = response.xpath("//div[@class='article__heading__title']").extract()[0]
        pub_time = response.xpath("//div[@class='meta-item article__heading__meta__left']/span/text()").extract()[0]
        website = response.xpath("//div[@class='article__heading__meta__source']/text()").extract()
        if website:
            website = website[0]
        else:
            website = ""
        content_html = response.xpath("//div[@class='node-article-content']").extract()[0]
        txtcont_text = response.xpath("//div[@class='node-article-content']/p/text()").extract()
        insert_info = {
            "title" : title,
            "_id" : response.meta['_id'],
            "url" : response.url,
            "content_html" : content_html,
            "source": '华尔街见闻',
            "website" : website,
            "pub_time" : pub_time,
            "craw_time" : now,
            "content_text" : txtcont_text,
        }
        insert_info_back = insert_info
        # _id = self.handler.insert_one('news', insert_info)
        yield SpiderItems(
            **insert_info_back
        )
