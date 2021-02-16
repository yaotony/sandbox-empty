from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import time
from LineMSG import linePush
from DataConn import getDBData
from StrategyData import BoxTheory,setDefault
from StrategyOrder import BoxTheoryOrderInp,BoxTheoryOrderOut,BoxTheoryOrderStop
# 定義要進出場的時間(9:00進場 13:30出場)
InTime=datetime.datetime.now().replace( hour=9 , minute=00 , second=00 , microsecond=00 )
OutTime=datetime.datetime.now().replace( hour=19 , minute=33 , second=00 , microsecond=00 )



starTime = datetime.datetime.strptime('2021-02-04 09:00:00','%Y-%m-%d %H:%M:%S')
endTime = datetime.datetime.strptime('2021-02-04 09:00:00','%Y-%m-%d %H:%M:%S')
endTimeTest = datetime.datetime.strptime('2021-02-04 13:30:00','%Y-%m-%d %H:%M:%S')
index = 1

InTime=starTime.replace( hour=10 , minute=00 , second=00 , microsecond=00 )


K = 60  #設定保留K線參數
L = 0 #取得筆數
r=0 #記錄交易資金流量
b=0 #設定多空方，多方=1，空方=-1，空手=0
topProfit = 0 
order_sign =0
boxIndex = 0

FUllData = getDBData(starTime,endTimeTest)


def job():
    global index,endTime,r,b,L,topProfit,order_sign,boxIndex
    index = index + 1
    endTime = (endTime + datetime.timedelta(minutes=1))
    print(index)
    print (endTime.strftime("%Y-%m-%d %H:%M:%S"))
   
    #定時回報 系統是否還在運行中
    if  index % 90 == 0 :
        linePush('我還在努力工作中.....')

    #取等每分鐘資料
    #df = getDBData(starTime,endTime)
    df  = FUllData[ FUllData['Time'] <= endTime].copy()
    BoxTheory(df,5,1)
    print(df)
    print('-------------------------------------------------')
    #row = df[df['Time'] > (endTime + datetime.timedelta(minutes=-1))]
    #L =len(df)-1
    #row = df.iloc[L]
    #print(row)

    if( endTime >= InTime ): 
        if b == 0 :
            r,b,order_sign,topProfit,boxIndex = BoxTheoryOrderInp(df,r,b,order_sign,topProfit,endTime,boxIndex)
        elif b == 1 or  b == -1 :
            (r,b,topProfit)=BoxTheoryOrderStop(df,0.5,-0.5,r,b,topProfit,endTime)

    

   #超過指定時間就停指下單，及清空所有口數
    #if datetime.datetime.now() > OutTime :
    if endTime > endTimeTest :
        if b != 0 :
                (r,b) = BoxTheoryOrderOut(df,r,b,endTime)
                topProfit=0
    
        linePush('時間到我要休息了.....')
        sched.shutdown(wait=False)
  


setDefault(FUllData)
# 定義BlockingScheduler
linePush('開始執行自動下單程式~')
sched = BlockingScheduler()
#每一分鐘執行一次 minute=1 ， 測試每5秒執行一次 seconds=5
sched.add_job(job, 'interval', seconds=1,max_instances=10) 
sched.start()

