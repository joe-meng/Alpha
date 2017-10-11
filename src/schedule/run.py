# coding: utf-8
import sys
import os

schedule_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(schedule_path)
if src_path not in sys.path:
    sys.path.append(src_path)

from share.contrib import import_string
from schedule.scheduler import get_scheduler
import conf


def runserver():
    scheduler = get_scheduler()
    for job in conf.jobs:
        import_string(job)
    try:
        print(scheduler.get_jobs())
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == '__main__':
    runserver()
