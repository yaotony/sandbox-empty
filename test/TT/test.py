from indicator import getFutureDailyInfo
from indicator import KBar
import pandas as pd
import time ,datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
from LineMSG import send_message

import math
import numpy as np
from Order2 import inp,outp,stop,stopByMA
from Strategy6 import BoxTheory
import os
import haohaninfo



# 定義交易商品
Product='MXFD1'
# 定義券商  、Simulator 虛擬期權
Broker='Simulator'


# 定義K棒物件
Today=datetime.datetime.now().strftime('%Y%m%d')
KBar1M=KBar(Today,1)

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()

FastPeriod=10
SlowPeriod=30 
starTime = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d')+' 15:00:00','%Y-%m-%d %H:%M:%S')
orderTime = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d')+' 15:30:00','%Y-%m-%d %H:%M:%S')
end_date = datetime.datetime.now() + datetime.timedelta(days=1)
endTime = datetime.datetime.strptime(end_date.strftime('%Y-%m-%d') +' 04:00:00','%Y-%m-%d %H:%M:%S')
#starTime = datetime.datetime.strptime(yy+'-'+mm+'-'+dd +' 08:45:00','%Y-%m-%d %H:%M:%S')
#orderTime = datetime.datetime.strptime(yy+'-'+mm+'-'+dd +' 09:30:00','%Y-%m-%d %H:%M:%S')
#endTime = datetime.datetime.strptime(yy+'-'+mm+'-'+dd +' 13:30:00','%Y-%m-%d %H:%M:%S')

print('starTime ',starTime)
print('orderTime ',orderTime)
print('endTime ',endTime)
for row in GO.Subscribe( Broker, 'match', Product ):
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    Qty=float(row[3])
    #print('當前價',Price,'，時間：',Time,'，量：',Qty)
    # 將資料填入K棒


    if Time < starTime :
            continue

    ChangeKFlag=KBar1M.AddPrice(Time,Price,Qty)
    
    # 每分鐘判斷一次
   
    if Time < orderTime :
            continue

    if ChangeKFlag==1:
        pf = pd.DataFrame(KBar1M.TAKBar,columns =['time','open','high','low','close','volume'])
        print('當前價',Price,'，時間：',Time,'，量：',Qty)
        pf = BoxTheory(pf,10,1)       
        pf = pf.sort_values(by=['time'],ascending=False)

        if(len(pf) < 2)  :
            continue

        BoxTop =pf['BoxTop'].iloc[1] 
        BoxDown =pf['BoxDown'].iloc[1] 

            
        FastMA=KBar1M.GetMAByOpen(FastPeriod,0)
        SlowMA=KBar1M.GetMAByOpen(SlowPeriod,0)

             
         
            

        if len(SlowMA)>=SlowPeriod+2:
                              
            Last1FastMA,Last2FastMA=FastMA[-3],FastMA[-2]
            Last1SlowMA,Last2SlowMA=SlowMA[-3],SlowMA[-2]  

            msg = ''
            msg_b = 0 
            if  Last1FastMA <  Last1SlowMA and  Last2FastMA > Last2SlowMA:#pf['ma_sign'].iloc[-1] == 1:
                msg_b = 1
                msg='黃金交叉 - 做多： Price:'+str(Price) +' '+Time.strftime("%Y-%m-%d %H:%M:%S")
            elif Last1FastMA >  Last1SlowMA and  Last2FastMA < Last2SlowMA:# pf['ma_sign'].iloc[-1] == -1:
                msg_b = -1
                msg='死亡交叉 - 做空： Price:'+str(Price)+' '+Time.strftime("%Y-%m-%d %H:%M:%S")
            elif   BoxTop < Last2FastMA  and BoxTop < Last2SlowMA :
                #print('BoxTop',BoxTop ,'Last2FastMA' ,Last2FastMA,'Last2SlowMA',Last2SlowMA)
                msg_b = 1
                msg='突破箱頂 - 做多： Price:'+str(Price)+' '+Time.strftime("%Y-%m-%d %H:%M:%S")
            elif    BoxDown > Last2FastMA  and BoxDown > Last2SlowMA :   
                #print('BoxDown',BoxDown ,'Last2FastMA' ,Last2FastMA,'Last2SlowMA',Last2SlowMA) 
                msg_b = -1
                msg='突破箱底 - 做空： Price:'+str(Price)+' '+Time.strftime("%Y-%m-%d %H:%M:%S")
                

            if msg_b!= 0 :
                saveDrawMap(KBar1M,Time.strftime("%Y%m%d%H%M%S"))
                status_code =  send_message(msg,'C:\\Temp\\'+Time.strftime("%Y%m%d%H%M%S")+'.png')
                if(status_code != 200):
                    send_message(msg)

  
       