#===============cron: 特定時間周期性地觸發===============
import time
from apscheduler.schedulers.blocking import BlockingScheduler

def job(text):
  t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
  print('{} --- {}'.format(text, t))

scheduler = BlockingScheduler()
# 在每天22點，每隔 1分鐘 執行一次 job 方法
scheduler.add_job(job, 'cron', hour=17, minute='*/1', args=['job1'])
# 在每天22和23點的25分，執行一次 job 方法
scheduler.add_job(job, 'cron', hour='22-23', minute='25', args=['job2'])

scheduler.start()