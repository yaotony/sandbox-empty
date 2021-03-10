from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import time
import pandas as pd
from LineMSG import linePush
from DataConn import getDBData,getDBDataForWebAPI
from StrategyData import BoxTheory,setDefault
from StrategyOrder import OrderInp,OrderOut,OrderStop
# 定義要進出場的時間(9:00進場 13:30出場)
InTime=datetime.datetime.now().replace( hour=9 , minute=00 , second=00 , microsecond=00 )
OutTime=datetime.datetime.now().replace( hour=19 , minute=33 , second=00 , microsecond=00 )



starTime = datetime.datetime.strptime('2021-02-25 09:00:00','%Y-%m-%d %H:%M:%S')
endTime = datetime.datetime.strptime('2021-02-25 09:00:00','%Y-%m-%d %H:%M:%S')
endTimeTest = datetime.datetime.strptime('2021-02-25 13:30:00','%Y-%m-%d %H:%M:%S')
index = 1

InTime=starTime.replace( hour=9 , minute=10 , second=00 , microsecond=00 )


K = 10  #設定保留K線參數
L = 0 #取得筆數
r=0 #記錄交易資金流量
b=0 #設定多空方，多方=1，空方=-1，空手=0
topProfit = 0 
order_sign =0
boxIndex = 0

FUllData = getDBDataForWebAPI(starTime,endTimeTest)

FUllData['Time'] = pd.to_datetime(FUllData['Time'], format='%Y-%m-%d %H:%M:%S')

result = pd.DataFrame({
        '最後報酬':[0],
        '總賺錢點數':[0],
        '總賠錢點數':[0],
        '交易次數':[0],
        '最大回檔':[0],
        '勝率':[0]
    })


def job():
    global index,endTime,r,b,L,topProfit,order_sign,boxIndex,result
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
            r,b,order_sign,topProfit,boxIndex,result = OrderInp(df,r,b,order_sign,topProfit,endTime,boxIndex,result)
        elif b == 1 or  b == -1 :
            (r,b,topProfit,result)=OrderStop(df,0.25,-0.5,r,b,topProfit,endTime,result)

    

   #超過指定時間就停指下單，及清空所有口數
    #if datetime.datetime.now() > OutTime :
    if endTime > endTimeTest :
        if b != 0 :
                (r,b,result) = OrderOut(df,r,b,endTime,result)
                topProfit=0
    
        
        sched.shutdown(wait=False)
        linePush('時間到我要休息了.....')
        linemsg =result.columns[0] +":"+str(result[result.columns[0]].iloc[0]) +',' +result.columns[1] +":"+str(result[result.columns[1]].iloc[0]) +',' +result.columns[2] +":"+str(result[result.columns[2]].iloc[0])+',' +result.columns[3] +":"+str(result[result.columns[3]].iloc[0])+',' +result.columns[4] +":"+str(result[result.columns[4]].iloc[0])+',' +result.columns[5] +":"+str(result[result.columns[5]].iloc[0])
        linePush( linemsg)
  


setDefault(FUllData)
# 定義BlockingScheduler
linePush('開始執行自動下單程式~')
sched = BlockingScheduler()
#每一分鐘執行一次 minute=1 ， 測試每5秒執行一次 seconds=5
sched.add_job(job, 'interval', seconds=1,max_instances=10) 
sched.start()

