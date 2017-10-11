# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# from spiders.db import MongoHandler

import logging
import time

import html2text
import pymongo
from scrapy import Request
from scrapy import Selector
from scrapy.utils.log import failure_to_exc_info
from scrapy.pipelines.files import FSFilesStore, S3FilesStore
from scrapy.pipelines.images import ImagesPipeline
from six.moves.urllib.parse import urljoin
from twisted.internet import defer

from websitespider.filesstore import AliOSSFilesStore
from websitespider.items import BaseItemWithPipeline, WechatItem
from websitespider.utils.utils import replace_url

logger = logging.getLogger(__name__)


class MongoPipeline(object):
    """写入 mongo
    """

    def __init__(self, mongo_uri, mongo_db, crawler):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            crawler=crawler,
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db][spider.settings['MONGO_COLLECTION']]
        spider.db = self.db

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        if not isinstance(item, BaseItemWithPipeline):
            return item

        item_mongo_id = self.db.insert_one(dict(item)).inserted_id

        if isinstance(item, WechatItem):
            # 微信公众号次级 post 处理
            if item['main_post_id']:
                # 如果是次级 post
                # 更新主 post 的 sub_posts, 标记为下载完毕
                self.db.update_one(
                    {'_id': item['main_post_id']},
                    {'$set': {('sub_posts.%s.id' % item['sub_post_index']): item_mongo_id}}
                )

            # 如果有次级 post
            for index, sub_post in enumerate(item['sub_posts']):
                self.crawler.engine.crawl(
                    Request(
                        url=urljoin(item['url'], sub_post['content_url']),
                        callback=spider.parse_detail,
                        meta={
                            'item': {
                                'thumb': [],
                                'wechat_post_id': None,
                                'website': sub_post['source_url'],
                                'sub_posts': [],
                                'main_post_id': item_mongo_id,
                                'sub_post_index': index,
                            }
                        }
                    ),
                    spider,
                )

        return item


class CNImagesPipeline(ImagesPipeline):
    """保存图片
    """

    STORE_SCHEMES = {
        '': FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'alioss': AliOSSFilesStore,
    }

    @classmethod
    def from_settings(cls, settings):
        cls.MIN_WIDTH = settings.getint('IMAGES_MIN_WIDTH', 0)
        cls.MIN_HEIGHT = settings.getint('IMAGES_MIN_HEIGHT', 0)
        cls.EXPIRES = settings.getint('IMAGES_EXPIRES', 90)
        cls.THUMBS = settings.get('IMAGES_THUMBS', {})
        s3store = cls.STORE_SCHEMES['s3']
        s3store.AWS_ACCESS_KEY_ID = settings['AWS_ACCESS_KEY_ID']
        s3store.AWS_SECRET_ACCESS_KEY = settings['AWS_SECRET_ACCESS_KEY']

        alioss_store = cls.STORE_SCHEMES['alioss']
        alioss_store.ALI_OSS_ACCESS_KEY_ID = settings['ALI_OSS_ACCESS_KEY_ID']
        alioss_store.ALI_OSS_ACCESS_KEY_SECRET = settings['ALI_OSS_ACCESS_KEY_SECRET']
        alioss_store.ALI_OSS_ENDPOINT = settings['ALI_OSS_ENDPOINT']
        alioss_store.ALI_OSS_BUCKET_NAME = settings['ALI_OSS_BUCKET_NAME']

        cls.IMAGES_URLS_FIELD = settings.get('IMAGES_URLS_FIELD', cls.DEFAULT_IMAGES_URLS_FIELD)
        cls.IMAGES_RESULT_FIELD = settings.get('IMAGES_RESULT_FIELD', cls.DEFAULT_IMAGES_RESULT_FIELD)
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri)

    def media_to_download(self, request, info):
        def _onsuccess(result):
            if not result:
                return  # returning None force download
            if isinstance(result, list):
                result = dict(result)
            last_modified = result.get('last_modified', None)
            if not last_modified:
                return  # returning None force download

            age_seconds = time.time() - last_modified
            age_days = age_seconds / 60 / 60 / 24
            if age_days > self.EXPIRES:
                return  # returning None force download

            referer = request.headers.get('Referer')
            logger.debug(
                'File (uptodate): Downloaded %(medianame)s from %(request)s '
                'referred in <%(referer)s>',
                {'medianame': self.MEDIA_NAME, 'request': request,
                 'referer': referer},
                extra={'spider': info.spider}
            )
            self.inc_stats(info.spider, 'uptodate')

            checksum = result.get('checksum', None)
            return {'url': request.url, 'path': path, 'checksum': checksum}

        path = self.file_path(request, info=info)
        dfd = defer.maybeDeferred(self.store.stat_file, path, info)
        dfd.addCallbacks(_onsuccess, lambda _: None)
        dfd.addErrback(
            lambda f:
            logger.error(self.__class__.__name__ + '.store.stat_file',
                         exc_info=failure_to_exc_info(f),
                         extra={'spider': info.spider})
        )
        return dfd

    def media_downloaded(self, response, request, info):
        result = super(CNImagesPipeline, self).media_downloaded(response, request, info)
        result['oss_url'] = 'http://chengjin-spider.oss-cn-shanghai.aliyuncs.com/%s' % result['path'].split('/')[-1]
        return result


class ThumbPipeline(CNImagesPipeline):
    """下载 thumb
    """

    DEFAULT_IMAGES_URLS_FIELD = 'thumb'
    DEFAULT_IMAGES_RESULT_FIELD = 'thumb'


class ImageSrcExtractPipeline(object):
    """从 html 中抽取图片地址
    """

    def process_item(self, item, spider):

        if not isinstance(item, BaseItemWithPipeline):
            return item

        image_urls = Selector(text=item['content_html']).xpath('//img/@src').extract()
        if 'image_urls' in item:
            item['image_urls'].extend(image_urls)
        else:
            item['image_urls'] = image_urls

        return item


class ImageSrcReplacePipeline(object):
    """替换原文 html 中图片地址
    """

    def process_item(self, item, spider):
        if not isinstance(item, BaseItemWithPipeline):
            return item

        if 'content_html' not in item:
            return item

        content_html = item['content_html']
        for image in item['images']:
            content_html = replace_url(content_html, image['url'], image['oss_url'])
        item['content_html'] = content_html
        return item


class HTML2TextPipeline(object):
    """提取 html 中的文字
    """

    def process_item(self, item, spider):
        if 'content_html' in item and not item.get('content_text', ''):
            item['content_text'] = html2text.html2text(item['content_html'])
        return item


class ItemFormatterPipeline(object):
    """规范 Item 字段
    """
    def process_item(self, item, spider):

        if not isinstance(item, BaseItemWithPipeline):
            return item

        if item.get('spider', ''):
            item['spider'] = spider.name

        item.update({
            "machine_class": "",
            "machine_summary": "",
            "machine_tags": "",
            "look_state": "0",
            "pub_state": "0",
            "push_state": "0",
        })

        return item

