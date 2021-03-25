# -*- coding: utf-8 -*-
import sys,datetime 
from order import Record
from indicator import getFutureDailyInfo
from indicator import KBar
import haohaninfo
import pandas as pd


# 定義交易商品
Product='MXFC1'
# 定義券商  、Simulator 虛擬期權
Broker='Simulator'


# 定義K棒物件
Today=datetime.datetime.now().strftime('%Y%m%d')
KBar1M=KBar(Today,1)

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
i = 0
for row in GO.Subscribe( Broker, 'match', Product ):
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    Qty=float(row[3])
    #print('當前價',Price,'，時間：',Time,'，量：',Qty)
    # 將資料填入K棒
    ChangeKFlag=KBar1M.AddPrice(Time,Price,Qty)
    
    # 每分鐘判斷一次
   
    
    if ChangeKFlag==1:
        print('ChangeKFlag：',ChangeKFlag)
        pf = pd.DataFrame(KBar1M.TAKBar,columns =['time','open','high','low','close','volume'])
        print('當前價',Price,'，時間：',Time,'，量：',Qty)
        print(pf)
        i = i + 1 
        if i > 20 :
            GO.EndSubscribe()

  
       