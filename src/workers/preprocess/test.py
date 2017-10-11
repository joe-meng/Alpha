
from apscheduler.schedulers.blocking import BlockingScheduler

# from other_preprocess.output import update_output
# from ctp_preprocess.day_handler import cal_day



sched = BlockingScheduler()



# @sched.scheduled_job("cron", second="*/3")
def my_job():
    print('hello world')



sched.add_job(my_job, 'cron', hour='16')

sched.start()