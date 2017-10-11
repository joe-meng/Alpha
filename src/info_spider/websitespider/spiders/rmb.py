# -*- coding: utf-8 -*-
import datetime
import hashlib
import scrapy
from scrapy.http import Request
from websitespider.items import SpiderItems
# from websitespider.utils.db import MysqlHnadler

class CnmnSpider(scrapy.Spider):
    name = "rmb"
    host = 'http://www.southmoney.com/'
    # handler = MysqlHnadler("foreign_exchange")
    def start_requests(self):
        urls = [
            'http://www.southmoney.com/waihui/rmb/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        * 解析新闻列表的第一页内容
        """
        url_list = []
        cur_url = response.url
        title_list = []
        li_list = response.xpath("//ul[@class='newslist']/li")
        url_list = response.xpath("//ul[@class='newslist']/li/a/@href").extract()
        date_list = response.xpath("//ul[@class='newslist']/li/span/text()").extract()
        for i in range(len(url_list)):
            title = response.xpath("//ul[@class='newslist']/li[position()=%s]/a/text()"%(i+1)).extract()
            if not title:
                title = response.xpath("//ul[@class='newslist']/li[position()=%s]/a/b/text()"%(i+1)).extract()
            title_list.append(title[0])
        for i in range(len(title_list)):
            url = self.host + url_list[i]
            title = title_list[i]
            date = date_list[i]
            if "日人民币汇率中间价最新公告" in title:
                yield Request(
                    url,
                    meta={
                        'title': title,
                        'pub_date': date.replace("/", "-"),
                    },
                    callback=self.parse_content,
                    dont_filter=False
                )

    def parse_content(self, response):
        # 解析新闻详情页面的内容
        now = datetime.datetime.now()
        content = response.xpath("//div[@class='articleCon']/p[position()=2]/text()").extract()[0]
        content.strip()
        # print(content)
        # try:
        #     daodu = content.xpath("//p[@class='p1 daodu']/text()").extract()[-1].strip()
        # except:
        #     daodu = ""
        # txtcont_html = content.xpath("//div[@id='txtcont']/p[position()=1]").extract()
        # txtcont_text = "".join(content.xpath("//div[@id='txtcont']/p[position()=1]/text()").extract())
        # if not txtcont_text:
        #     txtcont_text = "".join(content.xpath("//div[@id='txtcont']/p/text()").extract())
        # if not txtcont_text:
        #     txtcont_text = "".join(content.xpath("//div[@id='txtcont']/p/span/text()").extract())
        # if not txtcont_text:
        #     txtcont_text = "".join(content.xpath("//div[@id='txtcont']/p/span/span/text()").extract())
        # if not txtcont_text:
        #     txtcont_text = "".join(content.xpath("//div[@id='txtcont']/div/text()").extract())
        # actor = content.xpath("//p[@class='actor']/text()").extract()
        # actor = actor[0].replace("\r\n", "").strip() if actor else ""
        # insert_info = {
        #     "title" : response.meta['title'],
        #     "_id" : response.meta['_id'],
        #     "url" : response.url,
        #     "content_html" : txtcont_html,
        #     "abstract" : response.meta['abstract'],
        #     "source": response.meta['source'],
        #     "view" : view,
        #     "website" : header_list[0] if header_list else "",
        #     "author" : header_list[1] if len(header_list)>1 else "",
        #     "pub_time" : response.meta['pub_date'],
        #     "craw_time" : now,
        #     "category" : category,
        #     "actor" : actor,
        #     "daodu" : daodu,
        #     "content_text" : txtcont_text,
        # }
        # insert_info_back = insert_info
        # _id = self.handler.insert_one('news', insert_info)
        # yield SpiderItems(
        #     **insert_info_back
        # )
