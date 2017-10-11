# coding: utf-8
import scrapy
import hashlib
import datetime
import re
# import urllib
from lxml.html.clean import clean_html
from websitespider.utils.db import MongoHandler

def replace_url(html, func):

    def replace_href(matched):
        url = matched.group('url')
        href = func(url)
        href = href if href else url
        return 'href="%s"' % href

    def replace_src(matched):
        url = matched.group('url')
        src = func(url)
        src = src if src else url
        return 'src="%s"' % src

    _html = re.sub(r'href="(?P<url>.+)"', replace_href, html)
    _html = re.sub(r'src="(?P<url>.+)"', replace_src, _html)
    return _html


class ShmetSpider(scrapy.Spider):
    name = 'shmet'
    host = 'http://www.shmet.com'
    start_url = 'http://www.shmet.com/cms/_lastestitems.html'
    page_size = 10
    page_index = 2
    handler = MongoHandler()
    custom_settings = {
        'REDIRECT_ENABLED': False
    }

    def start_requests(self):
        url = '%s?%s' % (self.start_url, "pagesize=%s&pageindex=%s"%(self.page_size, self.page_index))
        yield scrapy.Request(url=url,
                             meta={'page_index': self.page_index},
                             callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//h5/a/@href').extract()
        for _url in urls:
            url = self.host + _url
            if self.has_crawl(url):
                print("exist",url)
            else:
                yield scrapy.http.Request(url, callback=self.parse_detail)

    def fix(self, url):
        url = url.group(1)
        if 'http://' not in url:
            return 'src="%s%s"' % (self.domain, url)
        else:
            return url

    def parse_detail(self, response):
        craw_time = datetime.datetime.now()
        content = response.xpath('//div[@class="tn-detail"]')
        html = response.xpath("//div[@class='tn-detail-text']").extract()[0]
        html = clean_html(html)
        html = re.sub(r'src="(.+?)"', self.fix, html)
        if '权限' in html and '登录' in html:
            print(" need access right")
            return
        title = content.xpath('//h1[@class="tn-title"]/text('
                              ')').extract()[0].replace("\r\n", "").strip()
        content_html = content.xpath('//div[@class="tn-detail-text"]').extract()[0]
        content_html = replace_url(content_html, response.urljoin)
        content_title = content.xpath('//div[@class="nm_content_all_title"]/text()').extract()
        content_title = ''.join(content_title)
        content_nr = content.xpath('//div[@class="nm_content_all_nr"]/text()').extract()
        content_nr = ''.join(content_nr)
        content_text = content_title + content_nr
        pub_time = content.xpath('//em[@class="tn-date"]/text()').extract()[0]
        view = content.xpath('//em[@class="tn-view"]/text()').re('.(\d+)')[0]
        category = content.xpath('//p[@class="tn-tags"]/span/a/text()').extract()
        actor = content.xpath('//div[@class="tn-editor tn-text-note"]'
                              '/text()').extract()[1].replace('\r\n', '').strip()
        website = content.xpath('//span[@class="tn-source"]/span/text()').extract()
        if website:
            website = website[0]
        else:
            website = ''
        news = {
            "title": title,
            "_id": self.get_id(response.url),
            "url": response.url,
            "content_html": content_html,
            "abstract": '',
            "source": '上海金属网',
            "view": view,
            "website": website,
            "author": '',
            "pub_time": pub_time,
            "craw_time": craw_time,
            "category": category,
            "actor": actor,
            "content_text": content_text,
        }
        self.handler.insert_one('news', news)

    def has_crawl(self, url):
        _id = self.get_id(url)
        flag = self.handler.check_exist("news", {"_id": _id})
        return flag

    @staticmethod
    def get_id(url):
        return hashlib.sha256(str(url).encode('utf-8')).hexdigest()
