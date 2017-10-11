# coding: utf-8
from apscheduler.schedulers.blocking import BlockingScheduler

from share.contrib import singleton


@singleton
def get_scheduler():
    return BlockingScheduler()
