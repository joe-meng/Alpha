
if __name__ == '__main__':
    import sys
    sys.path.append("../..")


from apscheduler.schedulers.blocking import BlockingScheduler

from other_preprocess.output import update_today_output
# from ctp_preprocess.day_handler import cal_day_info
from other_preprocess.month_re_cal import month_re_cal

sched = BlockingScheduler()


sched.add_job(update_today_output, 'cron', hour='17')
sched.add_job(month_re_cal, 'cron', hour='16', minute='*')


if __name__ == '__main__':
    sched.start()