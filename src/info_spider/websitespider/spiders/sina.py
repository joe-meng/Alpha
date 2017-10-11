# -*- coding: utf-8 -*-
import datetime
import hashlib
import scrapy
from scrapy.http import Request
from websitespider.items import SpiderItems
from websitespider.utils.db import MongoHandler

class CnmnSpider(scrapy.Spider):
    name = "sina"
    host = 'http://finance.sina.com.cn'
    handler = MongoHandler()
    start_urls = [
        # 'http://roll.finance.sina.com.cn/finance/qh/qsyw/index_1.shtml',
        # 'http://finance.sina.com.cn/futuremarket/comm_all.html',
        'http://roll.finance.sina.com.cn/finance/qh/pzyj/index.shtml',
    ]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        * 解析新闻列表的第一页内容
        """
        url_list = []
        cur_url = response.url
        # 解析列表内容
        url_list = response.xpath("//ul[@class='list_009']/li/a/@href").extract()
        title_list = response.xpath("//ul[@class='list_009']/li/a/text()").extract()
        for i in range(len(title_list)):
            if "futuremarket" in cur_url:
                url = self.host + url_list[i]
            else:
                url = url_list[i]
            _id = hashlib.sha256(url.encode('utf-8')).hexdigest()
            if self.handler.check_exist("news", {"_id": _id}):
                # 如果在数据库中已经存在  直接跳过
                continue
            else:
                # 处理数据库中不存在的
                yield Request(
                    url,
                    meta={
                        'title': title_list[i].strip(),
                        'source': 'sina',
                        'url': url,
                        '_id': _id,
                    },
                    callback=self.parse_content,
                    dont_filter=True
                )

    def parse_content(self, response):
        # 解析新闻详情页面的内容
        now = datetime.datetime.now()
        pub_time = response.xpath("//span[@class='time-source']/text()").extract()
        content = response.xpath("//div[@class='article article_16']")
        txtcont_html = content.extract()
        if "qhjspl" in response.url:
            txtcont_text = "".join(response.xpath("//div[@class='article article_16']/text()").extract())
        else:
            txtcont_text = "".join(response.xpath("//div[@class='article article_16']/p/text()").extract())
        insert_info = {
            "title" : response.meta['title'],
            "_id" : response.meta['_id'],
            "url" : response.url,
            "content_html" : txtcont_html,
            "source": response.meta['source'],
            "pub_time" : pub_time,
            "craw_time" : now,
            "content_text" : txtcont_text,
        }
        # _id = self.handler.insert_one('news', insert_info)
        yield SpiderItems(
            **insert_info
        )
