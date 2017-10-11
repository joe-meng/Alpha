# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from websitespider.items import SpiderItemWithPipeline


class GubaSpider(scrapy.Spider):
    name = 'guba'
    custom_settings = {
        'MONGO_COLLECTION': 'announcements'
    }
    start_urls = [
        'http://guba.eastmoney.com/list,600362,3,f.html',  # 江西铜业
        'http://guba.eastmoney.com/list,000630,3,f.html',  # 铜陵有色
        'http://guba.eastmoney.com/list,000878,3,f.html',  # 云南铜业
        'http://guba.eastmoney.com/list,601168,3,f.html',  # 西部矿业

        'http://guba.eastmoney.com/list,601600,3,f.html',  # 中国铝业
        'http://guba.eastmoney.com/list,hk01378,3,f.html',  # 中国宏桥
        'http://guba.eastmoney.com/list,600331,3,f.html',  # 宏达股份
        'http://guba.eastmoney.com/list,600497,3,f.html',  # 驰宏锌锗
        'http://guba.eastmoney.com/list,002114,3,f.html',  # 罗平锌电

        'http://guba.eastmoney.com/list,600432,3,f.html',  # 吉恩镍业
        'http://guba.eastmoney.com/list,000693,3,f.html',  # 华泽钴镍
        'http://guba.eastmoney.com/list,600112,3,f.html',  # 天成控股
    ]

    def parse(self, response):
        """
        * 解析新闻列表的第一页内容
        """
        posts = response.css('.articleh')
        for post in posts:
            post_url = post.css('.l3>a::attr(href)').extract_first('').strip()
            item = {
                'view': post.css('.l1::text').extract_first('').strip(),
                'title': post.css('.l3>a::text').extract_first('').strip(),
                'source': '',
                'author': post.css('.l4>a::text').extract_first('').strip(),
            }
            meta = {'item': item}
            yield scrapy.Request(url=response.urljoin(post_url), callback=self.parse_detail, meta=meta)

    def parse_detail(self, response):
        item = {
            'url': response.url,
            'pub_time': self.format_pub_time(response.css('.zwfbtime::text').re_first(r'\d.*\d')),
            'content_html': response.css('.zwcontentmain').extract_first('').strip(),
            'craw_time': datetime.now(),
            'attachments': [response.css('.zwtitlepdf>a::attr(href)').extract_first('').strip()],
        }
        item.update(response.meta.get('item', {}))

        yield SpiderItemWithPipeline(
            **item
        )

    def format_pub_time(self, pub_time):
        return datetime.strptime(pub_time, "%Y-%m-%d %H:%M:%S")
