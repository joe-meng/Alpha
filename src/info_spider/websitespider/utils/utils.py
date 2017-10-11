# -- coding: utf-8 --
import html

from scrapy.shell import inspect_response


def inspect_spider_response(response, spider):

    if spider.settings.get('DEBUG', True):
        return inspect_response(response, spider)


def replace_url(html, original_url, new_url):
    return html.replace(original_url, new_url)


def unescape_html(obj):
    if isinstance(obj, str):
        return html.unescape(obj)
    elif isinstance(obj, (list, tuple)):
        new_obj = []
        for i in obj:
            new_obj.append(unescape_html(i))
        return new_obj
    elif isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            new_obj[unescape_html(k)] = unescape_html(v)
        return new_obj
    return obj

