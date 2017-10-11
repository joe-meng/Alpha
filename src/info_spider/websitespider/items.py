# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SpiderItems(scrapy.Item):
    # mongodb 中的id
    _id = scrapy.Field()
    # 新闻标题
    title = scrapy.Field()
    # 爬虫要爬的网站
    source = scrapy.Field()
    # 新闻的原始地址
    url = scrapy.Field()
    # 新闻内容的含标签的正文
    content_html = scrapy.Field()
    # 爬虫抓取的摘要
    abstract = scrapy.Field()
    # 浏览量
    view = scrapy.Field()
    # 该文章的作者
    author = scrapy.Field()
    # 该文章的最初来源网站 （可能是转载的）
    website = scrapy.Field()
    # 发布时间
    pub_time = scrapy.Field()
    # 爬虫爬取时间
    craw_time = scrapy.Field()
    # 爬取的时候网站给的分类标签
    tag = scrapy.Field()
    # 分类
    category = scrapy.Field()
    # 责任编辑
    actor = scrapy.Field()
    # 文章的导读
    daodu = scrapy.Field()
    # 新闻内容的不含标签的正文
    content_text = scrapy.Field()


class BaseItemWithPipeline(scrapy.Item):
    """
    Item 基类
    """
    _id = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    content_html = scrapy.Field()
    abstract = scrapy.Field()
    view = scrapy.Field()
    author = scrapy.Field()
    website = scrapy.Field()
    pub_time = scrapy.Field()
    craw_time = scrapy.Field()
    tag = scrapy.Field()
    category = scrapy.Field()
    actor = scrapy.Field()
    daodu = scrapy.Field()
    content_text = scrapy.Field()

    # 图片相关, 类型为 list
    thumb = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

    # 附件, 类型为 list
    attachments = scrapy.Field()

    # 来自于哪个爬虫
    spider = scrapy.Field()

    # 数据状态初始化
    machine_class = scrapy.Field()
    machine_summary = scrapy.Field()
    machine_tags = scrapy.Field()
    look_state = scrapy.Field()
    pub_state = scrapy.Field()
    push_state = scrapy.Field()


# class SpiderItems(BaseItemWithPipeline):
#     """
#     * 爬虫的mongodb所要存储的一些字段
#     """
#     pass

class SpiderItemWithPipeline(BaseItemWithPipeline):
    pass


class WechatItem(BaseItemWithPipeline):
    """
    微信 Item, 比普通的类多几个字段
    """
    # 唯一标识、用于判重
    wechat_post_id = scrapy.Field()
    # 公众号名字
    wechat_username = scrapy.Field()
    # 同一条推送中的次级内容
    sub_posts = scrapy.Field()
    # 用于判断是否回写主 post 的 sub_posts
    main_post_id = scrapy.Field()
    sub_post_index = scrapy.Field()
