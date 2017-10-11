# -*- coding: utf-8 -*-
import datetime
import hashlib
import scrapy
from scrapy.http import Request
from websitespider.items import SpiderItems
from websitespider.utils.db import MongoHandler

class CnmnSpider(scrapy.Spider):
    name = "reset"
    host = 'http://www.cnmn.com.cn'
    handler = MongoHandler()
    def start_requests(self):
        urls = [
            'https://www.baidu.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        * 解析新闻列表的第一页内容

        """
        url_list = []
        cur_url = response.url
        # for line in self.handler.db.news.find({"content_text":"","machine_class":{"$ne":"Others"}}):
        #     url = line["url"]
        #     print("url:******************** ",url)
        #     yield Request(
        #         url,
        #         callback=self.parse_content,
        #         dont_filter=False
        #     )
        yield Request(
            "http://www.cnmn.com.cn/ShowNews1.aspx?id=372108",
            callback=self.parse_content,
            dont_filter=False
        )

    def parse_content(self, response):
        # 解析新闻详情页面的内容
        if "ShowNews1" not in response.url:
            # 过滤部分不需要的内容 重定向过来的 全部丢掉
            return
        now = datetime.datetime.now()
        content = response.xpath("//div[@class='container-p']")
        txtcont_text = "".join(content.xpath("//div[@id='txtcont']/p[position()=1]/text()").extract())
        if not txtcont_text:
            txtcont_text = "".join(content.xpath("//div[@id='txtcont']/p/text()").extract())
        if not txtcont_text:
            txtcont_text = "".join(content.xpath("//div[@id='txtcont']/p/span/text()").extract())
        if not txtcont_text:
            txtcont_text = "".join(content.xpath("//div[@id='txtcont']/p/span/span/text()").extract())
        if not txtcont_text:
            txtcont_text = "".join(content.xpath("//div[@id='txtcont']/div/text()").extract())
        insert_info = {
            "url" : response.url,
            "content_text" : txtcont_text,
        }
        insert_info_back = insert_info
        self.handler.db.news.update_one({"url":response.url}, {"$set":{"content_text":txtcont_text}})
        # _id = self.handler.insert_one('news', insert_info)
        yield SpiderItems(
            **insert_info_back
        )
