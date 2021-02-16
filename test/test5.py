import time
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', seconds=5)
def job1():
  t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
  print('job1 --- {}'.format(t))

@scheduler.scheduled_job('cron', second='*/7')
def job2():
  t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
  print('job2 --- {}'.format(t))

scheduler.start()