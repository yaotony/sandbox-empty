#===============interval: 固定時間間隔觸發===============
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from LineMSG import linePush

def job():
  print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 定義BlockingScheduler
sched = BlockingScheduler()
sched.add_job(job, 'interval', seconds=5) 
sched.start()