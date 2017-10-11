# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TempSpider(CrawlSpider):
    name = 'temp'
    allowed_domains = ['readfree.me']
    start_urls = ['http://readfree.me']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    def parse(self, response):
        i = {
            'thumb': ['https://img1.doubanio.com/mpic/s1598289.jpg'],
            'image_urls': ['https://img1.doubanio.com/mpic/s1598289.jpg'],
            'content_html': """<p style="max-width: 100%; min-height: 1em; line-height: 25.6px; text-align: center; box-sizing: border-box !important; word-wrap: break-word !important;"><img class=" " data-ratio="0.4981481481481482" data-s="300,640" data-src="http://mmbiz.qpic.cn/mmbiz/L7wQnPO2zhsQOKdRsHGE10E8rlATPGLLw8VE6WZhkN9reJGNfMXa6dRdvoNTF4CmoHa9CB1nuFr8icreeBFppTA/640?wx_fmt=png" data-type="png" data-w="540" width="auto" style="box-sizing: border-box !important; word-wrap: break-word !important; visibility: visible !important; width: auto !important; height: auto !important;" _width="auto" src="http://mmbiz.qpic.cn/mmbiz/L7wQnPO2zhsQOKdRsHGE10E8rlATPGLLw8VE6WZhkN9reJGNfMXa6dRdvoNTF4CmoHa9CB1nuFr8icreeBFppTA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1" data-fail="0"></p>"""
        }
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
