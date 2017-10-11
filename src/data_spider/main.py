# -- coding: utf-8 --
import inspect
import os
import sys

import django
import logging

import re
from apscheduler.schedulers.tornado import TornadoScheduler
from django.db import close_old_connections
from tornado.ioloop import IOLoop


def init_project():
    """
    初始化项目依赖
    :return:
    """
    root_path = os.path.abspath(__file__ if '__file__' in locals() else os.path.curdir)
    while os.path.basename(root_path).lower() != 'src':
        root_path = os.path.dirname(root_path)

    sys.path.append(os.path.join(root_path, 'api'))
    sys.path.append(root_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alpha.settings.prod")
    django.setup()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.info((' Init Django with profile: %s ' % os.environ.get('DJANGO_SETTINGS_MODULE')).center(80, '-'))


def spider_wrapper(fn):
    def wrapper():
        try:
            fn()
        except Exception as e:
            logging.error('wrapping spider: %s, error: %s' % (fn.__name__, e.args[0]))
        finally:
            close_old_connections()
    return wrapper


if __name__ == '__main__':
    init_project()

    # 设置 apscheduler 的 logging
    class AddedFilter(logging.Filter):
        def filter(self, record):
            return not record.msg.startswith('Adding') and not record.msg.startswith('Added')
    logging.getLogger("apscheduler.scheduler").addFilter(AddedFilter())

    import future_spider, spot_spider
    all_crawlers = []
    for spider in [future_spider, spot_spider]:
        submodules = inspect.getmembers(spider, inspect.ismodule)
        for submodule_name, submodule in submodules:
            crawlers = inspect.getmembers(submodule, lambda i: inspect.isfunction(i) and i.__name__.startswith('crawl_'))
            all_crawlers.extend(map(lambda i: i[1], crawlers))

    scheduler = TornadoScheduler()

    logging.info('爬取周期配置默认60分钟爬取一次, 如要指定1小时爬一次请在爬虫方法名最后加上 __60m, 目前支持 m 为单位的周期爬取, 储存、覆盖逻辑由爬虫自己实现')
    for crawler in all_crawlers:
        configuration = list(filter(lambda i: re.match(r'(\d+)(m)', i), crawler.__name__.split('__')))
        if not configuration:
            try:
                crawler()
            except:
                pass
            scheduler.add_job(spider_wrapper(crawler), 'interval', minutes=60, name=crawler.__name__, misfire_grace_time=5*60)
        else:
            duration, duration_type = re.match(r'(\d+)(m)', configuration[0]).groups()
            scheduler.add_job(crawler, 'interval', minutes=int(duration))

    scheduler.start()
    scheduler.print_jobs()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        IOLoop.instance().start()
    except (KeyboardInterrupt, SystemExit):
        pass
