# -*- coding: utf-8 -*-
import datetime
import hashlib
import scrapy
from scrapy.http import Request
from websitespider.items import SpiderItems
from websitespider.utils.db import MongoHandler

class CnmnSpider(scrapy.Spider):
    name = "cnmn"
    host = 'http://www.cnmn.com.cn'
    handler = MongoHandler()
    def start_requests(self):
        urls = [
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=13',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=19',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=43',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=271',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=272',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=273',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=274',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=276',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=278',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=279',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=865',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=876',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=877',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=878',
            'http://www.cnmn.com.cn/ShowNewsList.aspx?id=879',
            'http://www.cnmn.com.cn/metal.aspx?id=1&pageindex=1',
            'http://www.cnmn.com.cn/metal.aspx?id=16&pageindex=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        * 解析新闻列表的第一页内容
        """
        url_list = []
        cur_url = response.url
        if "metal" not in cur_url:
            # 处理金属类列表
            content = response.xpath('//div[@class="tab-pane active con-middle "]')
            title_list = content.xpath('//h4/a/text()').extract()
            time_list = content.xpath('//span[@class="time"]/text()').extract()
            abstract_list = content.xpath('//p/text()').extract()
            url_list = content.xpath('//h4/a/@href').extract()
        else:
            # 处理要闻类列表
            content = response.xpath('//div[@class="tab-pane con-middle active"]')
            title_list = content.xpath('//h4/a/text()').extract()
            time_list = content.xpath('//div/span[@class="time"]/text()').extract()
            abstract_list = content.xpath('//p/a/text()').extract()
            url_list = content.xpath('//h4/a/@href').extract()
        for i in range(len(title_list)):
            url = self.host+url_list[i]
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
                        'source': '中国有色网',
                        'pub_date': time_list[i],
                        'abstract': abstract_list[i],
                        'url': url,
                        '_id': _id,
                    },
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
        title = content.xpath("h4[@class='h4title']/text()").extract()
        view = content.xpath("//p[@class='info clearfix text-center']/span/span[@class='view']/text()").extract()
        header_list = content.xpath("//p[@class='info clearfix text-center']/span/a[@rel='tag']/text()").extract()
        # 标签  列表
        category = content.xpath("//p[@class='info clearfix text-center']/span/a[position()=2]/text()").extract()
        # category = category[0] if category else ""
        try:
            daodu = content.xpath("//p[@class='p1 daodu']/text()").extract()[-1].strip()
        except:
            daodu = ""
        txtcont_html = content.xpath("//div[@id='txtcont']/p[position()=1]").extract()
        txtcont_text = "".join(content.xpath("//div[@id='txtcont']/p/text()").extract())
        if not txtcont_text:
            txtcont_text = "".join(content.xpath("//div[@id='txtcont']/p/span/text()").extract())
        if not txtcont_text:
            txtcont_text = "".join(content.xpath("//div[@id='txtcont']/p/span/span/text()").extract())
        if not txtcont_text:
            txtcont_text = "".join(content.xpath("//div[@id='txtcont']/div/text()").extract())
        actor = content.xpath("//p[@class='actor']/text()").extract()
        actor = actor[0].replace("\r\n", "").strip() if actor else ""
        insert_info = {
            "title" : response.meta['title'],
            "_id" : response.meta['_id'],
            "url" : response.url,
            "content_html" : txtcont_html,
            "abstract" : response.meta['abstract'],
            "source": response.meta['source'],
            "view" : view,
            "website" : header_list[0] if header_list else "",
            "author" : header_list[1] if len(header_list)>1 else "",
            "pub_time" : response.meta['pub_date'],
            "craw_time" : now,
            "category" : category,
            "actor" : actor,
            "daodu" : daodu,
            "content_text" : txtcont_text,
        }
        insert_info_back = insert_info
        _id = self.handler.insert_one('news', insert_info)
        yield SpiderItems(
            **insert_info_back
        )
