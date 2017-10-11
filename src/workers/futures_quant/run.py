# -*- coding: utf-8 -*-

from cross_star import cross_star
from apscheduler.schedulers.blocking import BlockingScheduler
from settings import logger

def run():
    scheduler = BlockingScheduler()
    scheduler.add_job(cross_star, 'cron',hour='20', minute='01')
    scheduler.start()

if __name__ == "__main__":
    logger.info("十字星计算模块启动")
    run()


