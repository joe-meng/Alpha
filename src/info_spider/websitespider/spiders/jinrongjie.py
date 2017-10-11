# -*- coding: utf-8 -*-
import datetime
import hashlib
import scrapy
from scrapy.http import Request
from websitespider.items import SpiderItems
from websitespider.utils.db import MongoHandler

class JinRongJieSpider(scrapy.Spider):
    name = "jinrongjie"
    host = 'http://futures.jrj.com.cn/'
    allowed_domains = ["jrj.com.cn"]
    handler = MongoHandler()
    def start_requests(self):
        urls = [
            'http://futures.jrj.com.cn/list/jszx.shtml',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        * 解析新闻列表的第一页内容
        """
        url_list = []
        cur_url = response.url
        url_list = response.xpath("//ul[@class='jrj-l1 tab-ts jrj-f14']/li/label/a/@href").extract()
        title_list = response.xpath("//ul[@class='jrj-l1 tab-ts jrj-f14']/li/label/a/text()").extract()
        for i in range(len(url_list)):
            url = url_list[i]
            title = title_list[i]
            _id = hashlib.sha256(url.encode('utf-8')).hexdigest()
            if self.handler.check_exist("news", {"_id": _id}):
                # 如果在数据库中已经存在  直接跳过
                continue
            else:
                # 处理数据库中不存在的
                yield Request(
                    url,
                    meta={
                        'source': '金融界',
                        '_id': _id,
                        'title': title,
                    },
                    callback=self.parse_content,
                    dont_filter=False
                )

    def parse_content(self, response):
        # 解析新闻详情页面的内容
        now = datetime.datetime.now()
        info = response.xpath("//p[@class='inftop']/span/text()").extract()
        # print(info)
        if len(info)>6:
            # ['\r\n2017-06-05 16:55:45', '\r\n', '来源：', '黑金日志', '\r\n', '作者：', '董赟']
            pub_time = info[0].replace("\r", "").replace("\n", "")
            website = info[3]
            author = info[6]
        elif len(info)>5:
            # ['\r\n2017-06-05 16:55:45', '\r\n', '来源：',, '\r\n', '作者：', '董赟']
            pub_time = info[0].replace("\r", "").replace("\n", "")
            website = ""
            author = info[5]
        else:
            # ['\r\n2017-06-05 02:49:06', '\r\n', '来源：', '中国证券报', '\r\n']
            pub_time = info[0].replace("\r", "").replace("\n", "")
            website = info[3]
            author = ""
        content_html = "".join(response.xpath("//div[@class='texttit_m1']").extract())
        txtcont_text = "".join(response.xpath("//div[@class='texttit_m1']/p/text()").extract())
        insert_info = {
            "title" : response.meta['title'],
            "_id" : response.meta['_id'],
            "url" : response.url,
            "website" : website,
            "pub_time" : pub_time,
            "author" : author,
            "content_html" : content_html,
            "source": response.meta['source'],
            "craw_time" : now,
            "content_text" : txtcont_text,
        }
        _id = self.handler.insert_one('news', insert_info)
        yield SpiderItems(
            **{"_id":_id}
        )
