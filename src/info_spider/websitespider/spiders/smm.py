# -*- coding: utf-8 -*-
import datetime
import hashlib
import scrapy
from scrapy.http import Request
from websitespider.items import SpiderItems
from websitespider.utils.db import MongoHandler


class SmmSpider(scrapy.Spider):
    name = "smm"
    handler = MongoHandler()
    host = "https://news.smm.cn"

    def start_requests(self):
        urls = [
            "https://news.smm.cn/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        * 解析新闻列表的第一页内容
        """
        cur_url = response.url
        url_list = response.xpath("//div[@class='descBox']/h3/a/@href").extract()
        for url in url_list:
            if "platform" in url:
                continue
            url = self.host + url
            _id = hashlib.sha256(url.encode('utf-8')).hexdigest()
            if self.handler.check_exist("news", {"_id": _id}):
                # 如果在数据库中已经存在  直接跳过
                continue
            else:
                # 处理数据库中不存在的
                yield Request(
                    url,
                    meta={
                        '_id': _id,
                    },
                    callback=self.parse_content,
                    dont_filter=False
                )

    def parse_content(self, response):
        """
        * 解析文章内容
        """
        now = datetime.datetime.now()
        title_response = response.xpath("//div[@class='news-title']")
        title_html = title_response.extract()[0]
        title = title_response.xpath("//h1/text()").extract()[0]
        article_html = response.xpath("//article").extract()[0]
        article_list = response.xpath("//article/div/p/text()").extract()
        note = response.xpath("//div[@class='note']/text()").extract()[0]
        try:
            pub_date, website = note.split("来源")
            pub_date = pub_date.split("\n")[0]
        except:
            pub_date = ""
            website = ""
        insert_info = {
            "title" : title,
            "_id" : response.meta['_id'],
            "url" : response.url,
            "content_html" : title_html+article_html,
            "source": "上海有色网",
            "website" : website,
            "pub_time" : pub_date,
            "craw_time" : now,
            "content_text" : " ".join(article_list),
        }
        insert_info_back = insert_info
        _id = self.handler.insert_one('news', insert_info)
        yield SpiderItems(
            **insert_info_back
        )
