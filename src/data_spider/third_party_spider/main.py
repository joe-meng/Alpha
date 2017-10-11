# -- coding: utf-8 --
import os
from platform import platform

import django
import logging

import sys
from apscheduler.schedulers.tornado import TornadoScheduler
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

    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info((' Init Django with profile: %s ' % os.environ.get('DJANGO_SETTINGS_MODULE')).center(80, '-'))


if __name__ == '__main__':
    init_project()
    scheduler = TornadoScheduler()
    # 设置 apscheduler 的 logging
    class AddedFilter(logging.Filter):
        def filter(self, record):
            return not record.msg.startswith('Adding') and not record.msg.startswith('Added')

    logging.getLogger("apscheduler.scheduler").addFilter(AddedFilter())

    if platform().startswith('Windows'):
        from wind_spider import WindSpider

        # 命令行解析万德账号
        import argparse
        parser = argparse.ArgumentParser(description='运行爬虫')
        parser.add_argument('-w', '--wind_account', dest='wind_account', default='', help='指定万德账号')
        args = parser.parse_args()

        WindSpider(args.wind_account).run()
        scheduler.add_job(WindSpider(args.wind_account).run, 'cron', hour='18,22', minute='0', name='万德', misfire_grace_time=5*60)
    else:
        from enanchu_spider import EnanchuSpider
        from lingtong_spider import LingtongSpider
        from lgmi_spider import LGMISpider
        from shfe_spider import ShfeSpider
        from city_weather import city_weather
        from trade_order import trade_order
        from alert import main
        scheduler.add_job(ShfeSpider().run, 'interval', minutes=60, name='上期所', misfire_grace_time=5*60)
        scheduler.add_job(EnanchuSpider().run, 'interval', minutes=60, name='南储接口', misfire_grace_time=5*60)
        scheduler.add_job(LingtongSpider().run, 'interval', minutes=60, name='灵通报价', misfire_grace_time=5*60)
        scheduler.add_job(LGMISpider().run, 'interval', minutes=60, name='格兰钢铁', misfire_grace_time=5*60)
        scheduler.add_job(city_weather, 'cron', hour='3',minute='0', name='未来15天天气', misfire_grace_time=5*60)
        scheduler.add_job(trade_order, 'cron', hour='18',minute='5', name='持仓排名', misfire_grace_time=5*60)
        scheduler.add_job(main, 'interval', minutes=60, name='天气预警', misfire_grace_time=5*60)
    scheduler.start()
    scheduler.print_jobs()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        IOLoop.instance().start()
    except (KeyboardInterrupt, SystemExit):
        pass


